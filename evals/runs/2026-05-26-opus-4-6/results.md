# Skill Eval Result

- Run ID: `2026-05-26-opus-4-6`
- Model: `anthropic/opus-4-6`
- Agent: `vscode`
- Commit: `eaa9f4c25df53cf83807c91e9903af80f59f59f4`
- Total: **77.0/115.0 (67.0%)**
- Reward score: `79.0`; penalties: `-2.0`

## Per Skill

| Skill | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| ppp | 11.0 | 35.0 | 31.4% | 0.0 |
| ppp-cloud | 17.0 | 22.0 | 77.3% | 0.0 |
| shape | 24.0 | 33.0 | 72.7% | -2.0 |
| ship | 25.0 | 25.0 | 100.0% | 0.0 |

## Dimension Breakdown

| Dimension | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| Debug Loop | 0.0 | 4.0 | 0.0% | 0.0 |
| Diagnosis | 0.0 | 2.0 | 0.0% | 0.0 |
| Execution Discipline | 0.0 | 0.0 | 0.0% | 0.0 |
| Handoff | 0.0 | 4.0 | 0.0% | 0.0 |
| Interaction | 0.0 | 0.0 | 0.0% | 0.0 |
| Scope | 4.0 | 12.0 | 33.3% | 0.0 |
| Preferred Choice | 11.0 | 18.0 | 61.1% | 0.0 |
| Blocker Handoff | 12.0 | 18.0 | 66.7% | 0.0 |
| Inspection | 2.0 | 3.0 | 66.7% | 0.0 |
| Proof | 15.0 | 19.0 | 78.9% | 0.0 |
| Routing | 10.0 | 12.0 | 83.3% | -2.0 |
| Dependency Planning | 2.0 | 2.0 | 100.0% | 0.0 |
| Pattern Reuse | 2.0 | 2.0 | 100.0% | 0.0 |
| Reviewability | 7.0 | 7.0 | 100.0% | 0.0 |
| Risk Routing | 8.0 | 8.0 | 100.0% | 0.0 |
| Wave Planning | 4.0 | 4.0 | 100.0% | 0.0 |

## Cases

| Case | Skill | Score | Max | Percent | Penalties | Notes |
|---|---|---:|---:|---:|---:|---|
| ppp-cloud-auth-unclear | ppp-cloud | 12.0 | 12.0 | 100.0% | 0.0 |  |
| ppp-cloud-ui-empty-state | ppp-cloud | 5.0 | 10.0 | 50.0% | 0.0 |  |
| ppp-failing-test | ppp | 2.0 | 14.0 | 14.3% | 0.0 |  |
| ppp-proof-trap | ppp | 3.0 | 11.0 | 27.3% | 0.0 |  |
| ppp-small-bug | ppp | 6.0 | 10.0 | 60.0% | 0.0 |  |
| shape-clear-small-bug | shape | 3.0 | 8.0 | 37.5% | -2.0 |  |
| shape-large-feature | shape | 13.0 | 13.0 | 100.0% | 0.0 |  |
| shape-public-api-ambiguity | shape | 8.0 | 12.0 | 66.7% | 0.0 |  |
| ship-foundation-first | ship | 13.0 | 13.0 | 100.0% | 0.0 |  |
| ship-review-burden | ship | 12.0 | 12.0 | 100.0% | 0.0 |  |

## Weakest Dimensions

- `Handoff`: 0.0/4.0 (0.0%)
- `Diagnosis`: 0.0/2.0 (0.0%)
- `Debug Loop`: 0.0/4.0 (0.0%)
- `Scope`: 4.0/12.0 (33.3%)
- `Preferred Choice`: 11.0/18.0 (61.1%)

## Weakest Cases

- `ppp-failing-test` (ppp): 2.0/14.0 (14.3%)
- `ppp-proof-trap` (ppp): 3.0/11.0 (27.3%)
- `shape-clear-small-bug` (shape): 3.0/8.0 (37.5%)
- `ppp-cloud-ui-empty-state` (ppp-cloud): 5.0/10.0 (50.0%)
- `ppp-small-bug` (ppp): 6.0/10.0 (60.0%)

## Most Missed Criteria

- `keeps-first-pr-visible` (Scope): missed in 1 case(s)
- `preferred-main-proof-choice` (Preferred Choice): missed in 1 case(s)
- `targeted-test-choice` (Proof): missed in 1 case(s)
- `blocked-handoff-proof-gap` (Blocker Handoff): missed in 1 case(s)
- `blocked-handoff-resumable-next-step` (Blocker Handoff): missed in 1 case(s)
- `bounded-attempts` (Debug Loop): missed in 1 case(s)
- `classify-failure` (Diagnosis): missed in 1 case(s)
- `draft-pr-or-blocker-framing` (Handoff): missed in 1 case(s)
- `one-cause-per-attempt` (Debug Loop): missed in 1 case(s)
- `pr-review-handoff` (Handoff): missed in 1 case(s)

## Most Triggered Penalties

- `avoid-ship-on-clear-bug` (Routing): triggered in 1 case(s)
