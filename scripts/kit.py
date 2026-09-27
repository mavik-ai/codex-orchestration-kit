#!/usr/bin/env python3
"""Static, opt-in configuration installer. No network or model calls."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import tomllib
import uuid

TEMPLATES = Path(__file__).resolve().parents[1] / 'templates'
BEGIN = '<!-- codex-orchestration-kit:begin -->'
END = '<!-- codex-orchestration-kit:end -->'
PATHS = ('orchestration.config.toml', 'agents/sol-worker.toml',
         'agents/luna-explorer.toml', 'AGENTS.md')


def safe_path(path):
    """Reject symlinks, including broken links and ancestor links."""
    if '..' in path.parts:
        raise ValueError(f'Unsafe parent traversal: {path}')
    for item in (*reversed(path.parents), path):
        if item.is_symlink():
            raise ValueError(f'Symlink refused: {item}')
        if item.exists() and item != path and not item.is_dir():
            raise ValueError(f'Ancestor is not a directory: {item}')
    return path


def snapshot(path):
    safe_path(path)
    if not path.exists():
        return None, None
    if not path.is_file():
        raise ValueError(f'Not a regular file: {path}')
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_atomic(path, data, mode):
    safe_path(path)
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.kit-')
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def transaction(home, changes):
    before = {name: snapshot(home / name) for name in changes}
    applied = []
    try:
        for name, (data, mode) in changes.items():
            applied.append(name)
            write_atomic(home / name, data, mode)
    except Exception as error:
        failures = []
        for name in reversed(applied):
            try:
                write_atomic(home / name, *before[name])
            except Exception as rollback_error:
                failures.append(f'{name}: {rollback_error}')
        if failures:
            raise RuntimeError(f'{error}; rollback incomplete: {failures}; retain backup') from error
        raise


def marker_span(text):
    if not text.count(BEGIN) and not text.count(END):
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('AGENTS.md markers must form exactly one pair')
    start, end = text.index(BEGIN), text.index(END)
    if end < start:
        raise ValueError('AGENTS.md markers are reversed')
    return start, end + len(END)


def install(args, home):
    models = dict(COORDINATOR=args.coordinator, WORKER=args.worker, EXPLORER=args.explorer)
    for value in models.values():
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/-]*', value):
            raise ValueError('Invalid model ID')
    backups = safe_path(home / '.orchestration-kit/backups')
    if backups.exists() and not backups.is_dir():
        raise ValueError('Backup root must be a directory')
    changes, entries = {}, []
    for name in PATHS:
        original, mode = snapshot(home / name)
        text = (TEMPLATES / name).read_text(encoding='utf-8')
        for key, value in models.items():
            text = text.replace('{{' + key + '}}', value)
        if name.endswith('.toml'):
            tomllib.loads(text)
        else:
            block = text.strip()
            if marker_span(block) != (0, len(block)):
                raise ValueError('Invalid AGENTS.md template')
            # Preserve surrounding instructions byte-for-byte, including CRLF.
            current = original.decode('utf-8') if original is not None else ''
            span = marker_span(current)
            if span:
                text = current[:span[0]] + block + current[span[1]:]
            else:
                text = current + ('\n\n' if current else '') + block + '\n'
        data = text.encode('utf-8')
        if data == original:
            continue
        changes[name] = (data, mode if mode is not None else 0o600)
        entries.append(dict(path=name, original=None if original is None else
                            base64.b64encode(original).decode('ascii'), mode=mode, after=sha(data)))
    print(('Apply' if args.apply else 'Preview') + ': ' + (', '.join(changes) or 'no changes'))
    if not args.apply or not changes:
        return
    backup = backups / uuid.uuid4().hex
    backup.mkdir(parents=True, mode=0o700)
    manifest = dict(version=1, home=str(home), entries=entries)
    write_atomic(backup / 'manifest.json', json.dumps(manifest, indent=2).encode(), 0o600)
    print(f'Backup: {backup}')
    transaction(home, changes)


def restore(args, home):
    backup = safe_path(Path(args.backup).expanduser().absolute())
    root = safe_path(home / '.orchestration-kit/backups')
    if backup.parent != root or not backup.is_dir():
        raise ValueError('Backup must be a direct child of this home backup directory')
    manifest_path = safe_path(backup / 'manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('version') != 1 or manifest.get('home') != str(home):
        raise ValueError('Invalid backup version or home')
    entries = manifest.get('entries')
    if not isinstance(entries, list) or not entries or len(entries) > len(PATHS):
        raise ValueError('Invalid backup entries')
    changes = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid backup entry')
        name = entry.get('path')
        if not isinstance(name, str) or name not in PATHS or name in changes:
            raise ValueError('Unsafe or duplicate backup path')
        original, mode, after = entry.get('original'), entry.get('mode'), entry.get('after')
        if not isinstance(after, str) or not re.fullmatch('[0-9a-f]{64}', after):
            raise ValueError('Invalid backup hash')
        if original is None:
            if mode is not None:
                raise ValueError('Invalid absent-file mode')
            data = None
        else:
            if not isinstance(original, str) or type(mode) is not int or not 0 <= mode <= 0o7777:
                raise ValueError('Invalid original data or mode')
            data = base64.b64decode(original, validate=True)
        current, _ = snapshot(home / name)
        if current is None or sha(current) != after:
            raise ValueError(f'Later edits or missing file; restore refused: {name}')
        changes[name] = (data, mode)
    print(('Restore' if args.apply else 'Preview restore') + ': ' + ', '.join(changes))
    if args.apply:
        transaction(home, changes)


def doctor(home):
    for name in PATHS:
        data, _ = snapshot(home / name)
        if data is None:
            raise ValueError(f'Missing installed file: {name}')
        text = data.decode('utf-8')
        if name.endswith('.toml'):
            parsed = tomllib.loads(text)
            model = parsed.get('model')
            if not isinstance(model, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/-]*', model):
                raise ValueError(f'Invalid model: {name}')
            if name.startswith('agents/'):
                for key in ('name', 'description', 'developer_instructions'):
                    if not isinstance(parsed.get(key), str) or not parsed[key].strip():
                        raise ValueError(f'Missing role field {key}: {name}')
            else:
                agents = parsed.get('agents', {})
                if not isinstance(agents, dict) or agents.get('enabled') is not True or agents.get('max_concurrent_threads_per_session') != 2:
                    raise ValueError('Expected enabled agents and concurrency limit 2')
                worker = agents.get('default_subagent_model')
                if not isinstance(worker, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/-]*', worker):
                    raise ValueError('Invalid default worker model')
                print('Configured concurrent child limit: 2')
            print(f'OK TOML: {name}; configured model: {model}')
        elif marker_span(text) is None:
            raise ValueError('Missing AGENTS.md markers')
    print('Static checks only; no model access or runtime execution verified.')
    print('Select the installed profile with codex -p orchestration.')
    print('Agent roles and AGENTS.md apply across this CODEX_HOME; recursion policy is instructional.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('install', 'doctor', 'restore'):
        sub = commands.add_parser(command)
        sub.add_argument('--home', required=True)
        if command != 'doctor':
            sub.add_argument('--apply', action='store_true')
        if command == 'restore':
            sub.add_argument('--backup', required=True)
        if command == 'install':
            for role, default in [('coordinator', 'gpt-6-astra'), ('worker', 'gpt-6-sol'),
                                  ('explorer', 'gpt-6-luna')]:
                sub.add_argument('--' + role, default=default)
    args = parser.parse_args(argv)
    try:
        home = safe_path(Path(args.home).expanduser().absolute())
        if home.exists() and not home.is_dir():
            raise ValueError('Home must be a directory')
        if args.command == 'doctor':
            doctor(home)
        elif args.command == 'install':
            install(args, home)
        else:
            restore(args, home)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
