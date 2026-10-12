"""Labeled ServeWell tickets and a fixed, stratified dev/holdout split.

Dev is used for tuning prompts, thresholds and retrieval settings. Holdout is scored
once per release candidate, so reported numbers are not fitted to it. The unlabeled
chaos tickets form a separate adversarial set graded against hand-written expectations.
"""
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA_SET=ROOT/'data_set'
SPLIT_FILE=Path(__file__).resolve().parent/'split.json'
HOLDOUT_SHARE=0.3
SEED=20261012


def load(data_set=DATA_SET):
    """Return {ticket_id: {'ticket','index','label'}}; label is None for chaos tickets."""
    labels={x['ticket_id']:x for x in json.loads((data_set/'labels'/'train_labels.json').read_text(encoding='utf-8'))}
    cases={}
    with open(data_set/'tickets'/'train_index.csv',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            ticket=json.loads((data_set/'tickets'/'train'/(row['ticket_id']+'.json')).read_text(encoding='utf-8'))
            cases[row['ticket_id']]={'ticket':ticket,'index':row,'label':labels.get(row['ticket_id'])}
    return cases


def make_split(cases, holdout_share=HOLDOUT_SHARE, seed=SEED):
    # Stratify on category x routing so both sets keep the same mix of L1 and L2 work per domain.
    strata=defaultdict(list)
    for tid,case in sorted(cases.items()):
        if case['label']: strata[(case['ticket']['category'],case['label']['correct_routing'])].append(tid)
    rng=random.Random(seed);dev=[];holdout=[]
    for key in sorted(strata):
        ids=strata[key][:];rng.shuffle(ids);cut=round(len(ids)*holdout_share)
        holdout+=ids[:cut];dev+=ids[cut:]
    adversarial=sorted(tid for tid,case in cases.items() if not case['label'])
    return {'seed':seed,'holdout_share':holdout_share,'dev':sorted(dev),'holdout':sorted(holdout),'adversarial':adversarial}


def split(cases=None):
    """The committed split; create it once so every later run scores the same tickets."""
    if SPLIT_FILE.exists(): return json.loads(SPLIT_FILE.read_text(encoding='utf-8'))
    result=make_split(cases or load())
    SPLIT_FILE.write_text(json.dumps(result,indent=1),encoding='utf-8')
    return result


def select(cases, name, limit=None, per_category=None):
    ids=list(cases) if name=='all' else split(cases)[name]
    if per_category:
        # A small, balanced slice: the first N tickets of each category in the fixed split.
        taken=defaultdict(int);chosen=[]
        for tid in ids:
            category=cases[tid]['ticket']['category']
            if taken[category]<per_category: taken[category]+=1;chosen.append(tid)
        ids=chosen
    return ids[:limit] if limit else ids
