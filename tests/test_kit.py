import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('kit', Path(__file__).resolve().parents[1] / 'scripts/kit.py')
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)


class KitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / 'home'
        templates = self.root / 'templates'
        (templates / 'agents').mkdir(parents=True)
        (templates / 'orchestration.config.toml').write_text('model = "{{COORDINATOR}}"\n[agents]\nenabled = true\nmax_concurrent_threads_per_session = 2\ndefault_subagent_model = "{{WORKER}}"\n')
        for filename, model in [('sol-worker', 'WORKER'), ('luna-explorer', 'EXPLORER')]:
            (templates / f'agents/{filename}.toml').write_text(f'name = "{filename.replace("-", "_")}"\ndescription = "Task"\nmodel = "{{{{{model}}}}}"\ndeveloper_instructions = "No delegation"\n')
        (templates / 'AGENTS.md').write_text(kit.BEGIN + '\nInstructions\n' + kit.END + '\n')
        self.patcher = patch.object(kit, 'TEMPLATES', templates)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def run_cli(self, *args):
        return kit.main([args[0], '--home', str(self.home), *args[1:]])

    def install(self):
        self.assertEqual(self.run_cli('install', '--apply'), 0)
        return next((self.home / '.orchestration-kit/backups').iterdir())

    def test_preview_creates_nothing(self):
        self.assertEqual(self.run_cli('install'), 0)
        self.assertFalse(self.home.exists())

    def test_round_trip_preserves_bytes_modes_and_unrelated_files(self):
        self.home.mkdir()
        original = b'User instructions\r\n'
        (self.home / 'AGENTS.md').write_bytes(original)
        (self.home / 'AGENTS.md').chmod(0o640)
        (self.home / 'config.toml').write_text('untouched')
        backup = self.install()
        self.assertEqual(backup.stat().st_mode & 0o777, 0o700)
        self.assertEqual((backup / 'manifest.json').stat().st_mode & 0o777, 0o600)
        self.assertTrue((self.home / 'AGENTS.md').read_bytes().startswith(original))
        self.assertEqual(self.run_cli('install', '--apply'), 0)
        self.assertEqual(len(list(backup.parent.iterdir())), 1)
        self.assertEqual(self.run_cli('doctor'), 0)
        self.assertEqual(self.run_cli('restore', '--backup', str(backup)), 0)
        self.assertTrue((self.home / 'orchestration.config.toml').exists())
        self.assertEqual(self.run_cli('restore', '--backup', str(backup), '--apply'), 0)
        self.assertEqual((self.home / 'AGENTS.md').read_bytes(), original)
        self.assertEqual((self.home / 'AGENTS.md').stat().st_mode & 0o777, 0o640)
        self.assertFalse((self.home / 'orchestration.config.toml').exists())
        self.assertEqual((self.home / 'config.toml').read_text(), 'untouched')

    def test_later_edits_refuse_restore_without_partial_changes(self):
        backup = self.install()
        target = self.home / 'agents/luna-explorer.toml'
        target.write_text('later edit')
        self.assertEqual(self.run_cli('restore', '--backup', str(backup), '--apply'), 1)
        self.assertTrue((self.home / 'orchestration.config.toml').exists())
        self.assertEqual(target.read_text(), 'later edit')

    def test_symlink_target_and_backup_parent_rejected(self):
        self.home.mkdir()
        outside = self.root / 'outside'
        outside.mkdir()
        (self.home / 'agents').symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_cli('install', '--apply'), 1)
        self.assertEqual(list(outside.iterdir()), [])
        (self.home / 'agents').unlink()
        (self.home / '.orchestration-kit').symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_cli('install', '--apply'), 1)
        self.assertFalse((self.home / 'AGENTS.md').exists())

    def test_malformed_marker_and_model_are_rejected(self):
        self.home.mkdir()
        (self.home / 'AGENTS.md').write_text(kit.BEGIN)
        self.assertEqual(self.run_cli('install', '--apply'), 1)
        (self.home / 'AGENTS.md').unlink()
        self.assertEqual(self.run_cli('install', '--worker', 'bad"\n', '--apply'), 1)
        self.assertFalse((self.home / 'orchestration.config.toml').exists())

    def test_manifest_traversal_and_external_backup_rejected(self):
        backup = self.install()
        manifest = backup / 'manifest.json'
        data = json.loads(manifest.read_text())
        data['entries'][0]['path'] = '../outside'
        manifest.write_text(json.dumps(data))
        self.assertEqual(self.run_cli('restore', '--backup', str(backup), '--apply'), 1)
        self.assertEqual(self.run_cli('restore', '--backup', str(self.root), '--apply'), 1)

    def test_failure_rolls_back_original_files(self):
        self.home.mkdir()
        original = b'Keep me\n'
        (self.home / 'AGENTS.md').write_bytes(original)
        real_write = kit.write_atomic
        calls = 0

        def fail_once(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('injected disk error')
            return real_write(*args)

        with patch.object(kit, 'write_atomic', side_effect=fail_once):
            self.assertEqual(self.run_cli('install', '--apply'), 1)
        self.assertFalse((self.home / 'orchestration.config.toml').exists())
        self.assertEqual((self.home / 'AGENTS.md').read_bytes(), original)

    def test_doctor_rejects_missing_role_fields_and_wrong_limits(self):
        self.install()
        role = self.home / 'agents/sol-worker.toml'
        original = role.read_bytes()
        role.write_text('model = "gpt-6-sol"\n')
        self.assertEqual(self.run_cli('doctor'), 1)
        role.write_bytes(original)
        profile = self.home / 'orchestration.config.toml'
        profile.write_text(profile.read_text().replace('= 2', '= 3'))
        self.assertEqual(self.run_cli('doctor'), 1)

    def test_block_update_preserves_prefix_suffix(self):
        self.home.mkdir()
        original = b'Before\r\n' + (kit.BEGIN + '\nOld\n' + kit.END).encode() + b'\r\nAfter'
        target = self.home / 'AGENTS.md'
        target.write_bytes(original)
        self.install()
        self.assertEqual(target.read_bytes(), original.replace(b'Old', b'Instructions'))

    def test_invalid_toml_creates_nothing(self):
        (kit.TEMPLATES / 'agents/luna-explorer.toml').write_text('invalid = [')
        self.assertEqual(self.run_cli('install', '--apply'), 1)
        self.assertFalse(self.home.exists())

    def test_restore_failure_rolls_back_installed_state(self):
        backup = self.install()
        installed = {name: (self.home / name).read_bytes() for name in kit.PATHS}
        real_write = kit.write_atomic
        calls = 0

        def fail_once(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('restore disk error')
            return real_write(*args)

        with patch.object(kit, 'write_atomic', side_effect=fail_once):
            self.assertEqual(self.run_cli('restore', '--backup', str(backup), '--apply'), 1)
        self.assertEqual({name: (self.home / name).read_bytes() for name in kit.PATHS}, installed)


if __name__ == '__main__':
    unittest.main()
