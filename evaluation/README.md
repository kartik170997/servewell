# Evaluation

How we know the ServeWell support agent is accurate, safe and reliable, and why each
check exists. Results for a run are in `results/<run>/report.md`.

## Layers

| Layer | What it proves | How | Cost |
|---|---|---|---|
| 1. Deterministic tests | Rules that must never break: escalation gate (15 min + checklist), SLA timers, priority overrides, citation IDs, "never auto-complete a step", PII masking, checkpoint/resume | `pytest backend/tests` with the real LangGraph graph and SQLite, model mocked | Free, CI |
| 2. Offline evaluation | Quality of model judgement on labeled tickets | `python -m evaluation.run_eval ...` against an isolated instance | Claude + Pinecone usage |
| 3. Adversarial set | Behaviour on vague, misleading, contradictory or unknown-system tickets | Same harness, graded against per-type expectations | Same |
| 4. Production monitoring | Drift and real outcomes | MLflow ticket traces, accept/override rate, L2 bounce-backs | Ongoing |

Deterministic policy is implemented in Python and unit-tested; it is not left to the model and
not measured statistically. Model judgement (classification, planning, retrieval relevance) is
measured statistically because it is stochastic.

## Dataset and split

`data_set/` has 256 tickets. 220 are labeled with `correct_routing`, `should_escalate`,
`relevant_kb_docs`, `correct_resolution_summary` and a PASS/FAIL rubric. The 36 unlabeled tickets
are exactly the "chaos" tickets, so they form the adversarial set.

`split.json` is a fixed, seeded split stratified by category x routing: **155 dev / 65 holdout / 36 adversarial**.
Tune prompts, thresholds and retrieval settings on dev only. Score holdout once per release
candidate, so reported numbers are not fitted to it (this mirrors the unseen test cases the
reviewers will bring).

## Baselines (no model)

| Rule | Dev accuracy | Escalation recall | Unnecessary escalations |
|---|---|---|---|
| Always escalate | 66.5% | 100% | 100% |
| Ticket `escalation_flag` | 52.3% | 31.1% | 5.8% |
| Ticket already has troubleshooting history | 76.1% | 78.6% | 28.8% |

Accuracy alone is misleading: "always escalate" scores 66% while sending every basic ticket to L2,
which is the client's main pain point. We therefore report two error rates separately:

- **Missed escalation rate**: a store stays down longer (safety/revenue cost).
- **Unnecessary escalation rate**: L2 is loaded with L1 work (support cost).

The human-set `escalation_flag` agrees with the label only about half the time, and the
history rule is the real bar the agent must beat.

## Metrics

| Component | Metric | Label |
|---|---|---|
| Retrieval | Recall@5, Hit@5, MRR, matched by filename; ablation over lexical, vector, hybrid, rerank, tag filter, default score cutoffs | `relevant_kb_docs` |
| Escalation | Recall, precision, balanced accuracy, missed and unnecessary rates; by category and by "has history" | `should_escalate` |
| Routing | Confusion matrix of label vs first-turn route (`l1_guided`, `l2_escalation`, `needs_clarification`, `no_supported_step`) | `correct_routing` |
| Grounding | % steps with citations; % citing a labeled relevant document | `relevant_kb_docs` |
| Resolution quality | LLM judge PASS/PARTIAL/FAIL, routing appropriate, grounded, repeats attempted steps | `correct_resolution_summary`, `chaos_correct_behavior`, `evaluator_notes` |
| Operations | Error rate, p50/p95 latency; token and cache usage in MLflow | none |

Scoring choices:

- `sop/escalation-procedure.md` is the pinned procedure sent with every model call, not an
  indexed document, so it is excluded from retrieval recall instead of counting as a miss.
- Tickets are imported **as they arrived at intake**: `resolution_notes` are removed and status
  is reset to Open, so the agent cannot read the answer. Ticket history is kept because real
  intake includes it.
- The harness scores the agent's **first turn**. By design, routine escalation requires 15
  minutes of documented failed troubleshooting, so a label of `l2_escalation` for a ticket
  without an immediate trigger is expected to show as guided first. The report separates
  "escalated now" from "escalated or classified with an immediate trigger" and breaks results
  down by whether the ticket already has troubleshooting history.
- The LLM judge should be a different model from `CLAUDE_MODEL` to avoid self-grading. Before
  trusting it, hand-grade about 20 cases and report agreement.

## Running

```sh
python -m evaluation.make_instance                 # isolated copy in data/eval-instance
DATA_DIR=data/eval-instance MLFLOW_EXPERIMENT_NAME=folio-eval \
  uvicorn backend.main:app --env-file .env --host 127.0.0.1 --port 8011

python -m evaluation.run_eval baselines
python -m evaluation.run_eval retrieval --set dev --run retrieval-dev --base-url http://localhost:8011
python -m evaluation.run_eval workflow  --set dev --run dev-1 --base-url http://localhost:8011
python -m evaluation.run_eval workflow  --set adversarial --run dev-1 --base-url http://localhost:8011
python -m evaluation.run_eval judge     --run dev-1 --judge-model <different-model-id>
python -m evaluation.run_eval report    --run dev-1
```

The workflow command appends to `results/<run>/workflow.jsonl` and skips finished tickets, so an
interrupted run resumes. Evaluation tickets are named `EVAL-<run>-<ticket>` and live only in
the isolated instance; traces go to the `folio-eval` MLflow experiment.

## After deployment

1. Shadow mode: the agent proposes, L1 decides; track accept vs override per step.
2. Monitor L2 bounce-backs ("should have been L1"), reopened tickets, time to first meaningful
   response, latency, cost per ticket and prompt-cache hit rate from MLflow ticket traces.
3. Add every override and bounce-back to the golden set and rerun the dev evaluation before any
   prompt, procedure, retrieval or model change.

## Known limits

- First-turn only. A simulated-user replay (feeding step outcomes back) would measure full
  routine escalation, but a simulator that knows the label leaks the answer, so it needs care.
- The label vocabulary includes `non_it` and `needs_clarification`; the classifier has no
  `non_it` intent, so non-IT requests can only surface as clarification or a do-not-escalate category.
- One run per ticket. The model runs without a forced temperature, so repeat a subset to
  measure run-to-run variance before quoting small differences.
