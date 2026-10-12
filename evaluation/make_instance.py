"""Create an isolated evaluation data directory from the working workspace.

    python -m evaluation.make_instance            # -> data/eval-instance
    DATA_DIR=data/eval-instance MLFLOW_EXPERIMENT_NAME=folio-eval \
        uvicorn backend.main:app --env-file .env --host 127.0.0.1 --port 8011

The copy shares indexed documents, settings and the Pinecone namespace (read-only during
evaluation) but has its own tickets, checkpoints and traces, so hundreds of imported
EVAL- tickets never appear in the real workspace.
"""
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main(source=ROOT/'data', target=ROOT/'data'/'eval-instance'):
    if target.exists(): sys.exit(f'{target} already exists; delete it to start from a fresh copy.')
    target.mkdir(parents=True)
    # The backup API gives a consistent copy of a WAL-mode database that is in use.
    with sqlite3.connect(source/'folio.db') as src,sqlite3.connect(target/'folio.db') as dst: src.backup(dst)
    with sqlite3.connect(target/'folio.db') as c:
        for table in ('ticket_workflow','ticket_labels','ticket_history','tickets'): c.execute(f'DELETE FROM {table}')
    shutil.copytree(source/'uploads',target/'uploads')
    shutil.copy2(source/'.encryption-key',target/'.encryption-key')
    print(f'Created {target}')


if __name__=='__main__':
    main()
