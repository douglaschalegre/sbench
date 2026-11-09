from contextlib import closing
import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'prepare_turso_upload', Path(__file__).resolve().parents[1] / 'scripts/prepare_turso_upload.py'
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UploadTest(unittest.TestCase):
    def test_converts_delete_mode_without_changing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'source.sqlite', Path(directory) / 'upload.sqlite'
            with closing(sqlite3.connect(source)) as database:
                database.execute('CREATE TABLE answers (answer TEXT)')
                database.execute("INSERT INTO answers VALUES ('saved answer')")
                database.commit()
            before = source.read_bytes()
            module.prepare_upload(source, target)
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual(target.read_bytes()[18:20], bytes([2, 2]))
            with closing(sqlite3.connect(target)) as upload:
                self.assertEqual(upload.execute('PRAGMA journal_mode').fetchone(), ('wal',))
                self.assertEqual(upload.execute('SELECT * FROM answers').fetchall(), [('saved answer',)])
            with self.assertRaises(FileExistsError):
                module.prepare_upload(source, target)
            with self.assertRaises(FileExistsError):
                module.prepare_upload(source, source)
            self.assertEqual(source.read_bytes(), before)

    def test_includes_uncheckpointed_commits_in_a_standalone_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'source.sqlite', Path(directory) / 'upload.sqlite'
            with closing(sqlite3.connect(source)) as database:
                database.execute('PRAGMA journal_mode=WAL')
                database.execute('PRAGMA wal_autocheckpoint=0')
                database.execute('CREATE TABLE answers (answer TEXT)')
                database.execute("INSERT INTO answers VALUES ('pending WAL answer')")
                database.commit()
                self.assertGreater(Path(str(source) + '-wal').stat().st_size, 0)
                module.prepare_upload(source, target)
            self.assertFalse(Path(str(target) + '-wal').exists())
            with closing(sqlite3.connect(target)) as upload:
                self.assertEqual(upload.execute('SELECT * FROM answers').fetchall(), [('pending WAL answer',)])


if __name__ == '__main__':
    unittest.main()
