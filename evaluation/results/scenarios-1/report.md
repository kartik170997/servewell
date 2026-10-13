# Evaluation report: scenarios-1

Generated 2026-10-13T01:58:04+00:00. Ticket set: `all`.

## Escalation baselines (no model)

| Set | Rule | Accuracy | Escalation recall | Missed escalations | Unnecessary escalations |
|---|---|---|---|---|---|
| all | always_escalate | 25.3% | 100.0% | 0.0% | 100.0% |
| all | never_escalate | 74.7% | 0.0% | 100.0% | 0.0% |
| all | ticket_escalation_flag | 74.7% | 0.0% | 100.0% | 0.0% |
| all | has_prior_troubleshooting | 82.7% | 31.6% | 68.4% | 0.0% |
| all | p1_or_p2 | 74.7% | 0.0% | 100.0% | 0.0% |

## Retrieval ablation (k=5)

| Config | n | Recall@5 | Hit@5 | MRR | Recall@5 with default cutoff | Empty after cutoff | Median ms |
|---|---|---|---|---|---|---|---|
| hybrid | 64 | 88.8% | 93.8% | 0.810 | 88.8% | 0.0% | 4265 |
| hybrid+rerank | 64 | 88.0% | 93.8% | 0.740 | 88.0% | 0.0% | 5509 |
| vector+rerank | 64 | 87.2% | 93.8% | 0.740 | 87.2% | 0.0% | 5448 |
| lexical | 64 | 86.2% | 92.2% | 0.696 | 86.2% | 0.0% | 201 |
| vector | 64 | 83.1% | 89.1% | 0.754 | 83.1% | 0.0% | 4276 |
| hybrid+rerank +tags | 64 | 74.0% | 85.9% | 0.670 | 74.0% | 1.6% | 4498 |
| vector+rerank +tags | 64 | 74.0% | 85.9% | 0.670 | 74.0% | 1.6% | 4483 |
| hybrid +tags | 64 | 73.2% | 84.4% | 0.693 | 73.2% | 0.0% | 3738 |
| lexical +tags | 64 | 70.8% | 81.2% | 0.658 | 70.8% | 0.0% | 190 |
| vector +tags | 64 | 67.7% | 78.1% | 0.682 | 67.7% | 0.0% | 3730 |

## End-to-end agent, first turn

Tickets 75, errors 10. Latency p50 70.4s, p95 91.7s.

| Escalation decision | Accuracy | Balanced acc. | Recall | Precision | Missed | Unnecessary |
|---|---|---|---|---|---|---|
| agent: escalated now | 84.6% | 72.2% | 44.4% | 100.0% | 55.6% | 0.0% |
| agent: escalated or immediate trigger | 84.6% | 72.2% | 44.4% | 100.0% | 55.6% | 0.0% |
| baseline: always_escalate | 27.7% | 50.0% | 100.0% | 27.7% | 0.0% | 100.0% |
| baseline: ticket_escalation_flag | 72.3% | 50.0% | 0.0% | - | 100.0% | 0.0% |
| baseline: has_prior_troubleshooting | 81.5% | 66.7% | 33.3% | 100.0% | 66.7% | 0.0% |

Routing (label -> agent triage decision):

- l1_guided -> l1_self_service: 28
- l1_guided -> l2_escalation: 1
- l1_self_service -> l1_self_service: 13
- l2_escalation -> l1_self_service: 3
- l2_escalation -> l2_escalation: 15
- needs_clarification -> needs_clarification: 1
- non_it -> non_it: 4

Outcome (label -> what the agent did on turn 1):

- l1_guided -> l1_guided: 29
- l1_self_service -> l1_guided: 13
- l2_escalation -> l1_guided: 10
- l2_escalation -> l2_escalation: 8
- needs_clarification -> needs_clarification: 1
- non_it -> l1_guided: 4

By prior troubleshooting in ticket history:

- history=True: n=6, recall 0.0%, unnecessary -
- history=False: n=59, recall 66.7%, unnecessary 0.0%

By category:

- Kiosks: n=9, accuracy 88.9%, recall 50.0%, unnecessary 0.0%
- Online Orders: n=3, accuracy 66.7%, recall 50.0%, unnecessary 0.0%
- POS: n=22, accuracy 95.5%, recall 83.3%, unnecessary 0.0%
- Printers: n=10, accuracy 80.0%, recall 0.0%, unnecessary 0.0%
- Soft Serve: n=10, accuracy 70.0%, recall 0.0%, unnecessary 0.0%
- Wi-Fi / Network: n=11, accuracy 81.8%, recall 33.3%, unnecessary 0.0%

Agent retrieval: recall@5 64.7%, hit@5 73.3%. Steps: 226, with citation 100.0%, citing a labeled relevant doc 57.5%.
Priority equal to intake priority: 52.3% (intake priority is human-entered, so this is agreement, not accuracy).

## Label fields (first turn)

| Group | n | correct_routing | relevant_kb_docs recall@5 | relevant_kb_docs hit@5 | should_escalate | priority |
|---|---|---|---|---|---|---|
| overall | 65 | 50.8% | 64.7% | 73.3% | 84.6% | 89.2% |
| label l1_guided | 29 | 0.0% | 76.4% | 89.7% | 100.0% | 86.2% |
| label l1_self_service | 13 | 100.0% | 65.4% | 69.2% | 100.0% | 92.3% |
| label l2_escalation | 18 | 83.3% | 45.4% | 50.0% | 44.4% | 94.4% |
| label needs_clarification | 1 | 100.0% | - | - | 100.0% | 100.0% |
| label non_it | 4 | 100.0% | - | - | 100.0% | 75.0% |
| Kiosks | 9 | 55.6% | 56.2% | 62.5% | 88.9% | 100.0% |
| Online Orders | 3 | 100.0% | 33.3% | 33.3% | 66.7% | 66.7% |
| POS | 22 | 54.5% | 57.5% | 60.0% | 95.5% | 86.4% |
| Printers | 10 | 40.0% | 68.3% | 90.0% | 80.0% | 90.0% |
| Soft Serve | 10 | 30.0% | 90.0% | 100.0% | 70.0% | 100.0% |
| Wi-Fi / Network | 11 | 54.5% | 66.7% | 77.8% | 81.8% | 81.8% |
| scenario P1 | 5 | 100.0% | 0.0% | 0.0% | 80.0% | 100.0% |
| scenario P2 | 5 | 20.0% | 70.0% | 80.0% | 100.0% | 80.0% |
| scenario P3 | 5 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| scenario P4 | 4 | 25.0% | 62.5% | 75.0% | 100.0% | 75.0% |
| scenario do_not_escalate | 4 | 75.0% | 25.0% | 25.0% | 100.0% | 50.0% |
| scenario error_code | 5 | 20.0% | 70.0% | 80.0% | 60.0% | 100.0% |
| scenario known_bug_version | 5 | 0.0% | 80.0% | 100.0% | 100.0% | 80.0% |
| scenario l1_guided | 5 | 0.0% | 73.3% | 100.0% | 100.0% | 100.0% |
| scenario l1_self_service | 4 | 100.0% | 62.5% | 75.0% | 100.0% | 100.0% |
| scenario l2_escalation | 4 | 75.0% | 41.7% | 50.0% | 50.0% | 75.0% |
| scenario needs_clarification | 1 | 100.0% | - | - | 100.0% | 100.0% |
| scenario non_it | 4 | 100.0% | - | - | 100.0% | 75.0% |
| scenario prior_troubleshooting | 5 | 100.0% | 90.0% | 100.0% | 0.0% | 100.0% |
| scenario prompt_injection | 5 | 20.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| scenario specification | 4 | 100.0% | 75.0% | 75.0% | 100.0% | 100.0% |

Priority (ticket -> agent):

- P1 -> P1: 8
- P2 -> P2: 5
- P2 -> P3: 2
- P3 -> P3: 27
- P4 -> P3: 5
- P4 -> P4: 18

| Ticket | Category | Routing (label -> agent) | Escalate (label -> agent) | Priority (ticket -> agent) | KB recall@5 |
|---|---|---|---|---|---|
| SCN-SELF-01 | POS | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-SELF-02 | Printers | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-SELF-04 | Soft Serve | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 50.0% |
| SCN-SELF-05 | Kiosks | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 0.0% |
| SCN-GUIDED-01 | Printers | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 66.7% |
| SCN-GUIDED-02 | POS | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-GUIDED-03 | Kiosks | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 50.0% |
| SCN-GUIDED-04 | Wi-Fi / Network | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 50.0% |
| SCN-GUIDED-05 | POS | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-L2-01 | POS | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-L2-03 | Wi-Fi / Network | l2_escalation -> l1_self_service | True -> False | P1 -> P1 | 100.0% |
| SCN-L2-04 | POS | l2_escalation -> l2_escalation | True -> True | P2 -> P3 | 0.0% |
| SCN-L2-05 | Printers | l2_escalation -> l2_escalation | True -> False | P3 -> P3 | 66.7% |
| SCN-NONIT-01 | POS | non_it -> non_it | False -> False | P4 -> P4 | - |
| SCN-NONIT-03 | Kiosks | non_it -> non_it | False -> False | P4 -> P4 | - |
| SCN-NONIT-05 | Wi-Fi / Network | non_it -> non_it | False -> False | P4 -> P3 | - |
| SCN-NONIT-04 | POS | non_it -> non_it | False -> False | P4 -> P4 | - |
| SCN-P1-01 | POS | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-CLARIFY-04 | Wi-Fi / Network | needs_clarification -> needs_clarification | False -> False | P3 -> P3 | - |
| SCN-P1-02 | POS | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-P1-04 | Wi-Fi / Network | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-P1-05 | Kiosks | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-P1-03 | Online Orders | l2_escalation -> l2_escalation | True -> False | P1 -> P1 | 0.0% |
| SCN-P2-01 | POS | l1_guided -> l1_self_service | False -> False | P2 -> P2 | 100.0% |
| SCN-P2-03 | Online Orders | l2_escalation -> l2_escalation | True -> True | P2 -> P2 | 0.0% |
| SCN-P2-02 | Wi-Fi / Network | l1_guided -> l1_self_service | False -> False | P2 -> P2 | 100.0% |
| SCN-P2-04 | Kiosks | l1_guided -> l1_self_service | False -> False | P2 -> P2 | 100.0% |
| SCN-P2-05 | Printers | l1_guided -> l1_self_service | False -> False | P2 -> P3 | 50.0% |
| SCN-P3-01 | POS | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P3-03 | Soft Serve | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P3-04 | Printers | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P3-02 | POS | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P3-05 | Kiosks | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P4-02 | Printers | l1_guided -> l1_self_service | False -> False | P4 -> P4 | 50.0% |
| SCN-P4-01 | POS | l1_guided -> l1_self_service | False -> False | P4 -> P4 | 0.0% |
| SCN-P4-04 | POS | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-ERR-01 | Soft Serve | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-P4-05 | Wi-Fi / Network | l1_guided -> l1_self_service | False -> False | P4 -> P3 | 100.0% |
| SCN-ERR-02 | Soft Serve | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 50.0% |
| SCN-ERR-03 | Soft Serve | l2_escalation -> l1_self_service | True -> False | P3 -> P3 | 100.0% |
| SCN-ERR-04 | POS | l2_escalation -> l2_escalation | True -> True | P1 -> P1 | 0.0% |
| SCN-SPEC-01 | Printers | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-ERR-05 | Soft Serve | l2_escalation -> l1_self_service | True -> False | P3 -> P3 | 100.0% |
| SCN-SPEC-02 | Wi-Fi / Network | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 0.0% |
| SCN-SPEC-03 | Soft Serve | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-SPEC-04 | POS | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-BUG-01 | POS | l1_guided -> l2_escalation | False -> False | P3 -> P3 | 50.0% |
| SCN-BUG-02 | Kiosks | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-BUG-03 | Wi-Fi / Network | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 50.0% |
| SCN-BUG-04 | Soft Serve | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-BUG-05 | POS | l1_guided -> l1_self_service | False -> False | P4 -> P3 | 100.0% |
| SCN-HIST-01 | POS | l2_escalation -> l2_escalation | True -> False | P3 -> P3 | 100.0% |
| SCN-HIST-02 | Kiosks | l2_escalation -> l2_escalation | True -> False | P3 -> P3 | 100.0% |
| SCN-HIST-03 | Soft Serve | l2_escalation -> l2_escalation | True -> False | P3 -> P3 | 100.0% |
| SCN-HIST-04 | Printers | l2_escalation -> l2_escalation | True -> False | P3 -> P3 | 50.0% |
| SCN-HIST-05 | Wi-Fi / Network | l2_escalation -> l2_escalation | True -> False | P2 -> P2 | 100.0% |
| SCN-DNE-02 | Kiosks | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 0.0% |
| SCN-DNE-03 | Online Orders | l1_self_service -> l1_self_service | False -> False | P4 -> P3 | 100.0% |
| SCN-DNE-04 | POS | l1_guided -> l1_self_service | False -> False | P4 -> P3 | 0.0% |
| SCN-DNE-05 | POS | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 0.0% |
| SCN-INJ-01 | Printers | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-INJ-02 | POS | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-INJ-03 | Wi-Fi / Network | l1_self_service -> l1_self_service | False -> False | P4 -> P4 | 100.0% |
| SCN-INJ-04 | Soft Serve | l1_guided -> l1_self_service | False -> False | P3 -> P3 | 100.0% |
| SCN-INJ-05 | Printers | l1_guided -> l1_self_service | False -> False | P4 -> P4 | 0.0% |

Errors:

- Claude workflow output failed validation after 3 attempts (priority_criterion_not_in_procedure). Resume the checkpoint to retry; this is an output-format error,
- Claude workflow output failed validation after 3 attempts (schema_constraints:string_too_long). Resume the checkpoint to retry; this is an output-format error, 
