"""Import stores/assets CSV atomically; run python -m backend.import_directory."""
import csv
import json
from pathlib import Path
if __package__:
    from . import main
else:
    import main


def read_rows(path, required, key):
    with path.open(encoding='utf-8-sig', newline='') as file:
        reader=csv.DictReader(file)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'{path.name}: missing columns {sorted(required-set(reader.fieldnames or []))}')
        rows=[];seen=set()
        for number,row in enumerate(reader,2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'{path.name}:{number}: malformed CSV row')
            row={k:v.strip() for k,v in row.items()}
            if not all(row[k] for k in required): raise ValueError(f'{path.name}:{number}: required field is blank')
            if row[key] in seen: raise ValueError(f'{path.name}:{number}: duplicate {key}')
            seen.add(row[key]);rows.append(row)
        return rows


def import_directory(folder):
    folder=Path(folder)
    stores=read_rows(folder/'stores.csv', {'store_id','store_name'}, 'store_id')
    assets=read_rows(folder/'assets.csv', {'asset_id','store_id'}, 'asset_id')
    with main.ticket_workflow.LOCK, main.db() as c:
        known={r['store_id'] for r in c.execute('SELECT store_id FROM stores')}|{r['store_id'] for r in stores}
        missing={r['store_id'] for r in assets}-known
        if missing: raise ValueError(f'Assets reference unknown stores: {sorted(missing)}')
        # Validate first, then commit both tables together. Re-import updates by primary key.
        for r in stores:
            c.execute('INSERT INTO stores VALUES (?,?,?) ON CONFLICT(store_id) DO UPDATE SET store_name=excluded.store_name,payload=excluded.payload', (r['store_id'],r['store_name'],json.dumps(r)))
        for r in assets:
            c.execute('INSERT INTO assets VALUES (?,?,?) ON CONFLICT(asset_id) DO UPDATE SET store_id=excluded.store_id,payload=excluded.payload', (r['asset_id'],r['store_id'],json.dumps(r)))
    return {'stores':len(stores),'assets':len(assets)}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',nargs='?',default=str(Path(__file__).resolve().parents[1]/'datas'))
    args=parser.parse_args()
    print(json.dumps(import_directory(args.folder)))
