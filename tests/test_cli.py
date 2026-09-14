"""Exercise the public commands as subprocesses in isolated directories."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PV = ROOT / 'plugins/proof-to-video/skills/proof-to-video/scripts/pv.py'


class CliTests(unittest.TestCase):
    def call(self, *args):
        return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)

    def test_installed_skill_works_with_spaces_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='proof video ') as tmp:
            base = Path(tmp)
            install = self.call(ROOT/'scripts/install_skill.py', '--skills-dir', base/'skills')
            self.assertEqual(install.returncode, 0, install.stderr)
            installed = base/'skills/proof-to-video/scripts/pv.py'
            project = base/'my lesson'
            result = self.call(installed, 'init', project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.call(installed, 'validate', project).returncode, 0)
            before = (project/'project.json').read_bytes()
            self.assertNotEqual(self.call(installed, 'init', project).returncode, 0)
            self.assertEqual((project/'project.json').read_bytes(), before)
            self.assertNotEqual(self.call(ROOT/'scripts/install_skill.py', '--skills-dir', base/'skills').returncode, 0)

    def test_missing_models_fail_clearly(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)/'lesson'
            self.assertEqual(self.call(PV, 'init', project).returncode, 0)
            result = self.call(PV, 'audio', project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('--models', result.stderr)

    def test_all_commands_have_help(self):
        for command in ['init','doctor','validate','audio','render','verify','review','package']:
            with self.subTest(command=command):
                self.assertEqual(self.call(PV, command, '--help').returncode, 0)


if __name__ == '__main__':
    unittest.main()
