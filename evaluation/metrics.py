"""Pure scoring functions. No I/O, so they are unit-tested and reusable as MLflow scorers."""
from collections import defaultdict
from pathlib import PurePosixPath

# The escalation SOP is the pinned procedure given to every model call, not an indexed
# document. Labels that cite it are scored as "procedure cited", never as a retrieval miss.
PROCEDURE_DOC='escalation-procedure.md'


def kb_name(path):
    return PurePosixPath(str(path).replace('\\','/')).name.casefold()


def relevant_documents(label):
    return {kb_name(p) for p in label['relevant_kb_docs']}-{PROCEDURE_DOC}


def retrieval(relevant, ranked, k=5):
    """Recall/hit/precision at k and reciprocal rank over ranked filenames (duplicates collapsed)."""
    relevant={kb_name(x) for x in relevant}
    if not relevant: return None
    seen=[]
    for name in map(kb_name,ranked):
        if name not in seen: seen.append(name)
    top=seen[:k];found=relevant.intersection(top)
    rank=next((i for i,name in enumerate(seen,1) if name in relevant),None)
    return {'recall':len(found)/len(relevant),'hit':float(bool(found)),
            'precision':len(found)/k,'rr':1/rank if rank else 0.0}


def mean(rows, key):
    values=[r[key] for r in rows if r.get(key) is not None]
    return sum(values)/len(values) if values else None


def binary(pairs):
    """pairs: (expected, predicted) booleans where True is the positive class (escalate)."""
    tp=sum(1 for e,p in pairs if e and p);fp=sum(1 for e,p in pairs if not e and p)
    fn=sum(1 for e,p in pairs if e and not p);tn=sum(1 for e,p in pairs if not e and not p)
    ratio=lambda a,b:a/b if b else None
    recall=ratio(tp,tp+fn);specificity=ratio(tn,tn+fp);precision=ratio(tp,tp+fp)
    return {'n':len(pairs),'tp':tp,'fp':fp,'fn':fn,'tn':tn,'accuracy':ratio(tp+tn,len(pairs)),
            'recall':recall,'specificity':specificity,'precision':precision,
            'f1':ratio(2*precision*recall,precision+recall) if precision is not None and recall is not None else None,
            'balanced_accuracy':(recall+specificity)/2 if recall is not None and specificity is not None else None,
            # Missed escalations keep a store down; needless escalations load L2. Report both, not just accuracy.
            'missed_escalation_rate':ratio(fn,tp+fn),'unnecessary_escalation_rate':ratio(fp,fp+tn)}


def confusion(pairs):
    table=defaultdict(int)
    for expected,predicted in pairs: table[(expected,predicted)]+=1
    return {f'{e} -> {p}':n for (e,p),n in sorted(table.items())}


def by(rows, key, fn):
    groups=defaultdict(list)
    for r in rows: groups[r[key]].append(r)
    return {k:fn(v) for k,v in sorted(groups.items())}


def baseline_predictions(case):
    """Rules a reviewer will ask about: what does the system beat without any model?"""
    t=case['ticket']
    return {'always_escalate':True,'never_escalate':False,
            'ticket_escalation_flag':bool(t.get('escalation_flag')),
            'has_prior_troubleshooting':bool(t.get('ticket_history')),
            'p1_or_p2':t.get('priority') in ('P1','P2')}


def workflow_route(ticket):
    """Map a workflow ticket after its first agent turn onto the label's routing vocabulary."""
    w=ticket.get('workflow',{});kind=(w.get('pending') or {}).get('kind')
    if ticket.get('status')=='Escalated' or w.get('escalated_at'): return 'l2_escalation'
    if ticket.get('status')=='Resolved': return 'resolved'
    if kind=='step': return 'l1_guided'
    if kind in ('clarify','information'): return 'needs_clarification'
    return 'no_supported_step'
