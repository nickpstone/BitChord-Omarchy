"""Exercise the user-local installer without Java, network, or a desktop session."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class OmarchyInstallTest(unittest.TestCase):
    def test_install_upgrade_and_launch_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='bitchord install ') as directory:
            root = Path(directory)
            project = root / 'source'
            (project / 'scripts').mkdir(parents=True)
            shutil.copy(Path(__file__).parents[1] / 'omarchy', project / 'scripts/omarchy')
            icon = project / 'desktopApp/packaging/icons/AppIcon.png'
            icon.parent.mkdir(parents=True)
            icon.write_bytes(b'icon fixture')
            image = project / 'desktopApp/build/compose/binaries/main/app/BitChord'
            (image / 'bin').mkdir(parents=True)
            binary = image / 'bin/BitChord'
            binary.write_text('#!/bin/sh\nprintf "%s\\n" "$_JAVA_AWT_WM_NONREPARENTING" "$@"\n')
            binary.chmod(0o755)
            data = root / 'data files'
            bins = root / 'bin files'
            env = dict(os.environ, XDG_DATA_HOME=str(data), BITCHORD_BIN_HOME=str(bins))
            command = ['bash', str(project / 'scripts/omarchy'), 'install']
            subprocess.run(command, env=env, check=True, capture_output=True)
            entry = data / 'applications/bitchord.desktop'
            self.assertIn(f'Exec="{bins}/bitchord"', entry.read_text())
            self.assertIn('StartupWMClass=BitChord', entry.read_text())
            if shutil.which('desktop-file-validate'):
                subprocess.run(['desktop-file-validate', str(entry)], check=True)
            result = subprocess.run([str(bins / 'bitchord'), 'argument with spaces'], env=env,
                                    check=True, capture_output=True, text=True)
            self.assertEqual(result.stdout.splitlines(), ['1', 'argument with spaces'])
            stale = data / 'bitchord/app/obsolete.jar'
            stale.touch()
            settings = data / 'bitchord/keep-settings'
            settings.write_text('retained')
            subprocess.run(command, env=env, check=True, capture_output=True)
            self.assertFalse(stale.exists())
            self.assertEqual(settings.read_text(), 'retained')
            self.assertEqual(list((data / 'bitchord').glob('.install.*')), [])

    def test_missing_build_does_not_install(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir()
            shutil.copy(Path(__file__).parents[1] / 'omarchy', root / 'scripts/omarchy')
            result = subprocess.run(['bash', str(root / 'scripts/omarchy'), 'install'],
                                    env=dict(os.environ, XDG_DATA_HOME=str(root / 'data')),
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Build first', result.stderr)
            self.assertFalse((root / 'data').exists())


if __name__ == '__main__':
    unittest.main()
