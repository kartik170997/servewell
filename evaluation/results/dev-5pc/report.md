# Evaluation report: dev-5pc

Generated 2026-10-12T08:22:24+00:00. Ticket set: `dev`.

## Escalation baselines (no model)

| Set | Rule | Accuracy | Escalation recall | Missed escalations | Unnecessary escalations |
|---|---|---|---|---|---|
| dev | always_escalate | 66.5% | 100.0% | 0.0% | 100.0% |
| dev | never_escalate | 33.5% | 0.0% | 100.0% | 0.0% |
| dev | ticket_escalation_flag | 52.3% | 31.1% | 68.9% | 5.8% |
| dev | has_prior_troubleshooting | 76.1% | 78.6% | 21.4% | 28.8% |
| dev | p1_or_p2 | 50.3% | 40.8% | 59.2% | 30.8% |
| holdout | always_escalate | 66.2% | 100.0% | 0.0% | 100.0% |
| holdout | never_escalate | 33.8% | 0.0% | 100.0% | 0.0% |
| holdout | ticket_escalation_flag | 50.8% | 34.9% | 65.1% | 18.2% |
| holdout | has_prior_troubleshooting | 72.3% | 65.1% | 34.9% | 13.6% |
| holdout | p1_or_p2 | 46.2% | 23.3% | 76.7% | 9.1% |

## Retrieval ablation (k=5)

| Config | n | Recall@5 | Hit@5 | MRR | Recall@5 with default cutoff | Empty after cutoff | Median ms |
|---|---|---|---|---|---|---|---|
| hybrid | 30 | 66.3% | 96.7% | 0.841 | 66.3% | 0.0% | 4701 |
| vector+rerank | 30 | 62.4% | 100.0% | 0.906 | 62.4% | 0.0% | 5816 |
| hybrid+rerank | 30 | 61.6% | 100.0% | 0.906 | 61.6% | 0.0% | 5795 |
| lexical | 30 | 60.9% | 96.7% | 0.840 | 60.9% | 0.0% | 188 |
| vector | 30 | 60.8% | 93.3% | 0.880 | 60.8% | 0.0% | 4644 |
| hybrid+rerank +tags | 30 | 42.8% | 83.3% | 0.742 | 42.8% | 3.3% | 4530 |
| vector+rerank +tags | 30 | 42.8% | 83.3% | 0.742 | 42.8% | 3.3% | 4685 |
| vector +tags | 30 | 41.1% | 76.7% | 0.722 | 41.1% | 0.0% | 3888 |
| lexical +tags | 30 | 40.8% | 76.7% | 0.708 | 40.8% | 0.0% | 184 |
| hybrid +tags | 30 | 40.7% | 76.7% | 0.690 | 40.7% | 0.0% | 4102 |

## End-to-end agent, first turn

Tickets 30, errors 0. Latency p50 56.5s, p95 67.8s.

| Escalation decision | Accuracy | Balanced acc. | Recall | Precision | Missed | Unnecessary |
|---|---|---|---|---|---|---|
| agent: escalated now | 46.7% | 60.0% | 20.0% | 100.0% | 80.0% | 0.0% |
| agent: escalated or immediate trigger | 46.7% | 60.0% | 20.0% | 100.0% | 80.0% | 0.0% |
| baseline: always_escalate | 66.7% | 50.0% | 100.0% | 66.7% | 0.0% | 100.0% |
| baseline: ticket_escalation_flag | 40.0% | 52.5% | 15.0% | 75.0% | 85.0% | 10.0% |
| baseline: has_prior_troubleshooting | 70.0% | 70.0% | 70.0% | 82.4% | 30.0% | 30.0% |

Routing (label -> agent first turn):

- l1_guided -> l1_guided: 9
- l1_guided -> needs_clarification: 1
- l2_escalation -> l1_guided: 15
- l2_escalation -> l2_escalation: 4
- l2_escalation -> needs_clarification: 1

By prior troubleshooting in ticket history:

- history=True: n=17, recall 28.6%, unnecessary 0.0%
- history=False: n=13, recall 0.0%, unnecessary 0.0%

By category:

- Kiosks: n=5, accuracy 80.0%, recall 0.0%, unnecessary 0.0%
- Online Orders: n=5, accuracy 40.0%, recall 40.0%, unnecessary -
- POS: n=5, accuracy 40.0%, recall 0.0%, unnecessary 0.0%
- Printers: n=5, accuracy 40.0%, recall 0.0%, unnecessary 0.0%
- Soft Serve: n=5, accuracy 40.0%, recall 0.0%, unnecessary 0.0%
- Wi-Fi / Network: n=5, accuracy 40.0%, recall 40.0%, unnecessary -

Agent retrieval: recall@5 52.5%, hit@5 80.0%. Steps: 120, with citation 100.0%, citing a labeled relevant doc 72.5%.
Priority equal to intake priority: 30.0% (intake priority is human-entered, so this is agreement, not accuracy).
