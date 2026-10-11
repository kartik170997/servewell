"""Create a local workspace credential without overwriting existing configuration."""
from pathlib import Path
import secrets
p=Path('.env')
if p.exists():
    print('.env already exists; kept unchanged. Use its APP_TOKEN in Settings.')
else:
    p.write_text(Path('.env.example').read_text().replace('APP_TOKEN=', 'APP_TOKEN='+secrets.token_urlsafe(32), 1))
    p.chmod(0o600)
    print('Created .env. Open it and copy APP_TOKEN into Settings → Workspace connection.')
