"""Start MLflow, the FastAPI backend and the React frontend together, without Docker.

Run from the project folder with the virtual environment activated:  python start.py
Ctrl+C stops all three. If one of them exits, the others are stopped too.
"""
import argparse
import importlib.util
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
WINDOWS = os.name == 'nt'
COLORS = {'mlflow': '\033[35m', 'backend': '\033[36m', 'frontend': '\033[32m'}


def stream(name, proc):
    for line in iter(proc.stdout.readline, ''):
        sys.stdout.write(f"{COLORS.get(name, '')}[{name}]\033[0m {line}")
        sys.stdout.flush()


def start(name, command):
    proc = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            encoding='utf-8', errors='replace', bufsize=1,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if WINDOWS else 0,
                            start_new_session=not WINDOWS)
    threading.Thread(target=stream, args=(name, proc), daemon=True).start()
    return proc


def stop(proc):
    if proc.poll() is not None:
        return
    # uvicorn --reload and npm spawn child processes, so stop the whole tree.
    if WINDOWS:
        subprocess.call(['taskkill', '/T', '/F', '/PID', str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(10)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            os.killpg(proc.pid, signal.SIGKILL)


def wait_for_port(host, port, seconds):
    deadline = time.time() + seconds
    while time.time() < deadline:
        with socket.socket() as s:
            s.settimeout(1)
            if s.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--no-mlflow', action='store_true', help='do not start the MLflow tracking server')
    parser.add_argument('--no-reload', action='store_true', help='run the backend without auto-reload')
    parser.add_argument('--backend-port', default='8000')
    args = parser.parse_args()

    if WINDOWS:
        os.system('')  # enable ANSI colours in the Windows console
    if not (ROOT / '.env').exists():
        sys.exit('.env not found. Run "python setup.py" first, then fill in the provider keys.')
    missing = [m for m in ('dotenv', 'fastapi', 'uvicorn', 'mlflow', 'dspy', 'langgraph') if importlib.util.find_spec(m) is None]
    if missing:
        sys.exit(f'Python packages missing for {sys.executable}: {", ".join(missing)}.\n'
                 'Activate the virtual environment (.venv\\Scripts\\Activate.ps1 on Windows), then run:\n'
                 '  pip install -r backend/requirements.lock.txt')
    from dotenv import load_dotenv
    npm = 'npm.cmd' if WINDOWS else 'npm'
    if not (ROOT / 'node_modules').exists():
        print('node_modules not found; running "npm install" (first run only)...')
        try:
            if subprocess.call([npm, 'install'], cwd=ROOT) != 0:
                sys.exit('"npm install" failed; fix the error above and run start.py again.')
        except FileNotFoundError:
            sys.exit('npm not found. Install Node.js 22.13+ from https://nodejs.org and open a new terminal.')
    load_dotenv(ROOT / '.env')
    if not (ROOT / 'data' / 'folio.db').exists():
        import seed_data
        seed_data.restore()  # fresh clone: load the shared documents and tickets from seed/

    procs = {}
    mlflow_enabled = os.getenv('MLFLOW_ENABLED', 'false').strip().lower() in ('1', 'true', 'yes')
    if mlflow_enabled and not args.no_mlflow:
        uri = urlparse(os.getenv('MLFLOW_TRACKING_URI', 'http://127.0.0.1:5000'))
        host, port = uri.hostname or '127.0.0.1', uri.port or 5000
        procs['mlflow'] = start('mlflow', [sys.executable, '-m', 'backend.mlflow_server', '--host', host, '--port', str(port)])
        # Start the backend only once MLflow accepts connections, so the first traces are not lost.
        if not wait_for_port(host, port, 60):
            print(f'MLflow did not open {host}:{port} within 60 s; starting the backend anyway.')

    backend = [sys.executable, '-m', 'uvicorn', 'backend.main:app', '--env-file', '.env', '--port', args.backend_port]
    procs['backend'] = start('backend', backend if args.no_reload else backend + ['--reload'])
    procs['frontend'] = start('frontend', [npm, 'run', 'dev'])

    print('\nFrontend http://localhost:5173 | Backend http://localhost:%s/docs%s\nPress Ctrl+C to stop all.\n'
          % (args.backend_port, ' | MLflow http://localhost:5000' if 'mlflow' in procs else ''))
    try:
        while True:
            for name, proc in procs.items():
                if proc.poll() is not None:
                    print(f'\n{name} exited with code {proc.returncode}; stopping the others.')
                    return proc.returncode or 1
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nStopping...')
        return 0
    finally:
        for proc in procs.values():
            stop(proc)


if __name__ == '__main__':
    sys.exit(main())
