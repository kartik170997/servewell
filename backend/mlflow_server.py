"""Run Folio's persistent local MLflow UI and tracking server."""
import argparse
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    load_dotenv(root/'.env')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',default='127.0.0.1');parser.add_argument('--port',default='5000')
    args=parser.parse_args()
    data=Path(os.getenv('DATA_DIR',root/'data')).resolve();data.mkdir(parents=True,exist_ok=True)
    command=[sys.executable,'-m','mlflow','server','--backend-store-uri','sqlite:///'+(data/'mlflow.db').as_posix(),
        '--artifacts-destination',str(data/'mlflow-artifacts'),'--host',args.host,'--port',args.port,'--workers','1']
    raise SystemExit(subprocess.call(command))
