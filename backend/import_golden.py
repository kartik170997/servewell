"""Import reviewed JSONL cases into a native MLflow GenAI evaluation dataset."""
import argparse
import json
import os
from pathlib import Path
from dotenv import load_dotenv


def read_records(path):
    records=[];ids=set()
    for line_no,line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        inputs=row.get('inputs');expectations=row.get('expectations')
        if not isinstance(inputs,dict) or not str(inputs.get('query','')).strip() or not isinstance(expectations,dict) or not expectations:
            raise ValueError(f'Line {line_no}: inputs.query and nonempty expectations are required.')
        if row.get('tags',{}).get('status')=='example-only-not-reviewed': raise ValueError('Replace example labels with reviewed golden answers before importing.')
        case_id=inputs.get('case_id')
        if not case_id or case_id in ids: raise ValueError(f'Line {line_no}: provide a unique inputs.case_id.')
        ids.add(case_id);records.append(row)
    if not records: raise ValueError('Dataset is empty.')
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path');parser.add_argument('--name',default='folio-golden-workflows')
    parser.add_argument('--dataset-id',help='Merge into an existing dataset instead of creating one.')
    args=parser.parse_args();records=read_records(args.path)
    load_dotenv(Path(__file__).resolve().parents[1]/'.env')
    import mlflow
    import mlflow.genai
    uri=os.environ['MLFLOW_TRACKING_URI'];name=os.environ['MLFLOW_EXPERIMENT_NAME']
    mlflow.set_tracking_uri(uri);experiment=mlflow.set_experiment(name)
    dataset=mlflow.genai.get_dataset(args.dataset_id) if args.dataset_id else mlflow.genai.create_dataset(name=args.name,experiment_id=experiment.experiment_id,tags={'purpose':'human-reviewed-workflow-evaluation'})
    dataset.merge_records(records)
    print(json.dumps({'dataset_id':dataset.dataset_id,'records_submitted':len(records)}))


if __name__=='__main__': main()
