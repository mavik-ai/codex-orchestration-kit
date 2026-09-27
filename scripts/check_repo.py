#!/usr/bin/env python3
"""Offline checks for public content, templates and local Markdown links."""
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=ROOT,
    text=True,
).splitlines()
errors = []
for name in sorted(set(paths)):
    path = ROOT / name
    if not path.is_file():
        continue
    if path.suffix in {'.jsonl', '.pem', '.key'} or path.name in {'auth.json', '.env'}:
        errors.append(f'{name}: private artifact extension/name')
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        errors.append(f'{name}: unexpected binary; review before publishing')
        continue
    for pattern in [r'/(?:Users|home)/[a-zA-Z0-9_-]+/', r'gh[pousr]_[A-Za-z0-9]{30,}',
                    r'github_pat_[A-Za-z0-9_]{30,}', r'sk-(?:proj-)?[A-Za-z0-9_-]{35,}',
                    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']:
        if re.search(pattern, text):
            errors.append(f'{name}: possible private path/credential; inspect locally')
    if path.suffix == '.md':
        for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{name}: broken or escaping local link: {href}')
for path in (ROOT / 'templates').rglob('*.toml'):
    text = path.read_text()
    for key in ('COORDINATOR', 'WORKER', 'EXPLORER'):
        text = text.replace('{{' + key + '}}', 'example-model')
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        errors.append(f'{path.relative_to(ROOT)}: invalid rendered TOML: {exc}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'Public-content checks, TOML templates and local links passed ({len(set(paths))} files).')
