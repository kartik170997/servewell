"""Share the local workspace data through git as a seed snapshot.

  python seed_data.py export    copy data/ -> seed/ (run before committing)
  python seed_data.py restore   copy seed/ -> data/ (start.py does this automatically on a fresh clone)

The snapshot holds documents, tickets, the store/asset directory, procedure versions, workflow
checkpoints and the original uploads. It deliberately leaves out:
  - saved provider settings (the encrypted API keys) and .encryption-key; a clone uses its own .env
  - mlflow.db and ticket-traces.sqlite (traces are machine-local; mlflow.db is over GitHub's 100 MB limit)
Search vectors stay in Pinecone, so the clone must use the same index host and namespace in .env.
"""
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
SEED = ROOT / 'seed'
DATABASES = ('folio.db', 'workflow-checkpoints.sqlite')


def copy_db(src, dst):
    # The backup API gives a consistent copy even while the app is running in WAL mode.
    dst.unlink(missing_ok=True)
    with sqlite3.connect(f'file:{src.as_posix()}?mode=ro', uri=True) as s, sqlite3.connect(dst) as d:
        s.backup(d)
    sqlite3.connect(dst).close()


def export():
    if not (DATA / 'folio.db').exists():
        sys.exit('data/folio.db not found; nothing to export.')
    if SEED.exists():
        shutil.rmtree(SEED)
    SEED.mkdir()
    for name in DATABASES:
        if (DATA / name).exists():
            copy_db(DATA / name, SEED / name)
    con = sqlite3.connect(SEED / 'folio.db')
    con.execute('DELETE FROM settings')  # encrypted provider keys never leave this machine
    con.commit()
    con.execute('VACUUM')
    con.close()
    shutil.copytree(DATA / 'uploads', SEED / 'uploads')
    with sqlite3.connect(SEED / 'folio.db') as c:
        docs = c.execute('SELECT count(*) FROM documents').fetchone()[0]
        tickets = c.execute('SELECT count(*) FROM tickets').fetchone()[0]
    print(f'Exported {docs} documents and {tickets} tickets to seed/. Commit the seed/ folder to share them.')


def restore(force=False):
    if not (SEED / 'folio.db').exists():
        return False
    if (DATA / 'folio.db').exists() and not force:
        print('data/folio.db already exists; seed not restored (use "restore --force" to overwrite).')
        return False
    DATA.mkdir(exist_ok=True)
    for name in DATABASES:
        for suffix in ('', '-wal', '-shm'):
            (DATA / (name + suffix)).unlink(missing_ok=True)
        if (SEED / name).exists():
            shutil.copy2(SEED / name, DATA / name)
    shutil.copytree(SEED / 'uploads', DATA / 'uploads', dirs_exist_ok=True)
    print('Restored seed data into data/. Provider keys come from .env.')
    return True


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action == 'export':
        export()
    elif action == 'restore':
        if not restore(force='--force' in sys.argv) and not (SEED / 'folio.db').exists():
            sys.exit('seed/folio.db not found.')
    else:
        sys.exit(__doc__)
