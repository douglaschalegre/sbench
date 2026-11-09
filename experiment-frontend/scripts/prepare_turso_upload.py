"""Create a self-contained SQLite snapshot in WAL mode for Turso upload."""

import argparse
from contextlib import closing
import os
from pathlib import Path
import sqlite3


def prepare_upload(source: Path, destination: Path) -> None:
    # Reserve a new file so a mistaken path cannot overwrite the source or a backup.
    descriptor = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    try:
        with closing(sqlite3.connect(source.resolve().as_uri() + '?mode=ro', uri=True)) as original:
            with closing(sqlite3.connect(destination)) as snapshot:
                # The backup API includes committed data still present in the source WAL.
                original.backup(snapshot)
                mode = snapshot.execute('PRAGMA journal_mode=WAL').fetchone()[0]
                if mode != 'wal':
                    raise RuntimeError(f'Unexpected journal mode: {mode}')
                busy, _, _ = snapshot.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone()
                if busy:
                    raise RuntimeError('Could not checkpoint the upload snapshot.')
                if snapshot.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise RuntimeError('Upload snapshot failed integrity_check.')
    except BaseException:
        for suffix in ('', '-wal', '-shm'):
            destination.with_name(destination.name + suffix).unlink(missing_ok=True)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    prepare_upload(args.source, args.destination)
    print(f'Upload snapshot ready: {args.destination} (journal_mode=WAL)')
