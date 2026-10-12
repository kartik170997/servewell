# Evaluation report: first-turn-5pc

Generated 2026-10-12T14:02:36+00:00. Ticket set: `all`.

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

## End-to-end agent, first turn

Tickets 30, errors 0. Latency p50 76.9s, p95 84.3s.

| Escalation decision | Accuracy | Balanced acc. | Recall | Precision | Missed | Unnecessary |
|---|---|---|---|---|---|---|
| agent: escalated now | 50.0% | 52.2% | 18.8% | 60.0% | 81.2% | 14.3% |
| agent: escalated or immediate trigger | 50.0% | 52.2% | 18.8% | 60.0% | 81.2% | 14.3% |
| baseline: always_escalate | 53.3% | 50.0% | 100.0% | 53.3% | 0.0% | 100.0% |
| baseline: ticket_escalation_flag | 46.7% | 48.7% | 18.8% | 50.0% | 81.2% | 21.4% |
| baseline: has_prior_troubleshooting | 70.0% | 70.5% | 62.5% | 76.9% | 37.5% | 21.4% |

Routing (label -> agent first turn):

- l1_guided -> l1_guided: 10
- l1_guided -> l2_escalation: 3
- l1_guided -> needs_clarification: 2
- l2_escalation -> l1_guided: 13
- l2_escalation -> l2_escalation: 2

By prior troubleshooting in ticket history:

- history=True: n=13, recall 20.0%, unnecessary 0.0%
- history=False: n=17, recall 16.7%, unnecessary 18.2%

By category:

- Kiosks: n=5, accuracy 60.0%, recall 33.3%, unnecessary 0.0%
- Online Orders: n=5, accuracy 40.0%, recall 33.3%, unnecessary 50.0%
- POS: n=5, accuracy 40.0%, recall 0.0%, unnecessary 33.3%
- Printers: n=5, accuracy 60.0%, recall 0.0%, unnecessary 0.0%
- Soft Serve: n=5, accuracy 40.0%, recall 0.0%, unnecessary 0.0%
- Wi-Fi / Network: n=5, accuracy 60.0%, recall 33.3%, unnecessary 0.0%

Agent retrieval: recall@5 53.8%, hit@5 76.7%. Steps: 109, with citation 100.0%, citing a labeled relevant doc 72.5%.
Priority equal to intake priority: 33.3% (intake priority is human-entered, so this is agreement, not accuracy).

## Label fields (first turn)

| Group | n | correct_routing | relevant_kb_docs recall@5 | relevant_kb_docs hit@5 | should_escalate | priority |
|---|---|---|---|---|---|---|
| overall | 30 | 40.0% | 53.8% | 76.7% | 50.0% | 33.3% |
| label l1_guided | 15 | 66.7% | 57.3% | 80.0% | 86.7% | 33.3% |
| label l2_escalation | 15 | 13.3% | 50.3% | 73.3% | 13.3% | 33.3% |
| Kiosks | 5 | 20.0% | 46.7% | 80.0% | 60.0% | 20.0% |
| Online Orders | 5 | 40.0% | 44.6% | 60.0% | 40.0% | 20.0% |
| POS | 5 | 40.0% | 20.0% | 40.0% | 40.0% | 20.0% |
| Printers | 5 | 60.0% | 83.0% | 100.0% | 60.0% | 20.0% |
| Soft Serve | 5 | 20.0% | 64.3% | 100.0% | 40.0% | 60.0% |
| Wi-Fi / Network | 5 | 60.0% | 64.3% | 80.0% | 60.0% | 60.0% |

Priority (ticket -> agent):

- P2 -> P1: 3
- P2 -> P2: 5
- P2 -> P3: 2
- P3 -> P1: 2
- P3 -> P2: 2
- P3 -> P3: 5
- P4 -> P1: 1
- P4 -> P2: 2
- P4 -> P3: 8

| Ticket | Category | Routing (label -> agent) | Escalate (label -> agent) | Priority (ticket -> agent) | KB recall@5 |
|---|---|---|---|---|---|
| INC-00038 | Kiosks | l1_guided -> l1_guided | False -> False | P4 -> P3 | 66.7% |
| INC-00062 | Kiosks | l2_escalation -> l1_guided | True -> False | P4 -> P3 | 75.0% |
| INC-00056 | Kiosks | l1_guided -> l2_escalation | True -> True | P2 -> P1 | 0.0% |
| INC-00314 | Kiosks | l2_escalation -> l1_guided | True -> False | P2 -> P2 | 25.0% |
| INC-00094 | Kiosks | l1_guided -> needs_clarification | False -> False | P4 -> P2 | 66.7% |
| INC-00020 | Online Orders | l2_escalation -> l2_escalation | True -> True | P2 -> P1 | 0.0% |
| INC-00040 | Online Orders | l1_guided -> l1_guided | False -> False | P4 -> P3 | 100.0% |
| INC-00022 | Online Orders | l2_escalation -> l1_guided | True -> False | P2 -> P2 | 80.0% |
| INC-00117 | Online Orders | l1_guided -> l2_escalation | False -> True | P4 -> P3 | 0.0% |
| INC-00023 | Online Orders | l2_escalation -> l1_guided | True -> False | P2 -> P1 | 42.9% |
| INC-00004 | POS | l1_guided -> l2_escalation | False -> True | P3 -> P1 | 0.0% |
| INC-00001 | POS | l2_escalation -> l1_guided | True -> False | P4 -> P3 | 0.0% |
| INC-00008 | POS | l1_guided -> l1_guided | False -> False | P3 -> P2 | 50.0% |
| INC-00007 | POS | l2_escalation -> l1_guided | True -> False | P3 -> P3 | 0.0% |
| INC-00015 | POS | l1_guided -> l1_guided | False -> False | P3 -> P2 | 50.0% |
| INC-00029 | Printers | l1_guided -> l1_guided | False -> False | P3 -> P3 | 60.0% |
| INC-00016 | Printers | l2_escalation -> l1_guided | True -> False | P4 -> P3 | 80.0% |
| INC-00031 | Printers | l1_guided -> l1_guided | False -> False | P4 -> P1 | 100.0% |
| INC-00041 | Printers | l2_escalation -> l1_guided | True -> False | P4 -> P2 | 75.0% |
| INC-00058 | Printers | l1_guided -> l1_guided | False -> False | P2 -> P3 | 100.0% |
| INC-00026 | Soft Serve | l2_escalation -> l1_guided | True -> False | P2 -> P3 | 75.0% |
| INC-00017 | Soft Serve | l1_guided -> l1_guided | False -> False | P3 -> P3 | 66.7% |
| INC-00053 | Soft Serve | l2_escalation -> l1_guided | True -> False | P4 -> P3 | 80.0% |
| INC-00021 | Soft Serve | l1_guided -> needs_clarification | False -> False | P3 -> P3 | 33.3% |
| INC-00079 | Soft Serve | l2_escalation -> l1_guided | True -> False | P2 -> P2 | 66.7% |
| INC-00012 | Wi-Fi / Network | l2_escalation -> l2_escalation | True -> True | P3 -> P1 | 0.0% |
| INC-00081 | Wi-Fi / Network | l1_guided -> l1_guided | False -> False | P2 -> P2 | 66.7% |
| INC-00013 | Wi-Fi / Network | l2_escalation -> l1_guided | True -> False | P2 -> P2 | 75.0% |
| INC-00103 | Wi-Fi / Network | l1_guided -> l1_guided | False -> False | P3 -> P3 | 100.0% |
| INC-00025 | Wi-Fi / Network | l2_escalation -> l1_guided | True -> False | P4 -> P3 | 80.0% |
