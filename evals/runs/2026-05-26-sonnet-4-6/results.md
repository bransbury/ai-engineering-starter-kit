# Skill Eval Result

- Run ID: `2026-05-26-sonnet-4-6`
- Model: `anthropic/sonnet-4-6`
- Agent: `vscode`
- Commit: `2b02289cfb29cf0cec60c219cecf35271271f9a7`
- Total: **80.0/115.0 (69.6%)**
- Reward score: `80.0`; penalties: `0.0`

## Per Skill

| Skill | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| ppp | 21.0 | 35.0 | 60.0% | 0.0 |
| ppp-cloud | 22.0 | 22.0 | 100.0% | 0.0 |
| shape | 12.0 | 33.0 | 36.4% | 0.0 |
| ship | 25.0 | 25.0 | 100.0% | 0.0 |

## Dimension Breakdown

| Dimension | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| Debug Loop | 0.0 | 4.0 | 0.0% | 0.0 |
| Execution Discipline | 0.0 | 0.0 | 0.0% | 0.0 |
| Interaction | 0.0 | 0.0 | 0.0% | 0.0 |
| Blocker Handoff | 8.0 | 18.0 | 44.4% | 0.0 |
| Handoff | 2.0 | 4.0 | 50.0% | 0.0 |
| Scope | 6.0 | 12.0 | 50.0% | 0.0 |
| Preferred Choice | 11.0 | 18.0 | 61.1% | 0.0 |
| Risk Routing | 6.0 | 8.0 | 75.0% | 0.0 |
| Routing | 9.0 | 12.0 | 75.0% | 0.0 |
| Proof | 18.0 | 19.0 | 94.7% | 0.0 |
| Dependency Planning | 2.0 | 2.0 | 100.0% | 0.0 |
| Diagnosis | 2.0 | 2.0 | 100.0% | 0.0 |
| Inspection | 3.0 | 3.0 | 100.0% | 0.0 |
| Pattern Reuse | 2.0 | 2.0 | 100.0% | 0.0 |
| Reviewability | 7.0 | 7.0 | 100.0% | 0.0 |
| Wave Planning | 4.0 | 4.0 | 100.0% | 0.0 |

## Cases

| Case | Skill | Score | Max | Percent | Penalties | Notes |
|---|---|---:|---:|---:|---:|---|
| ppp-cloud-auth-unclear | ppp-cloud | 12.0 | 12.0 | 100.0% | 0.0 |  |
| ppp-cloud-ui-empty-state | ppp-cloud | 10.0 | 10.0 | 100.0% | 0.0 |  |
| ppp-failing-test | ppp | 4.0 | 14.0 | 28.6% | 0.0 |  |
| ppp-proof-trap | ppp | 11.0 | 11.0 | 100.0% | 0.0 |  |
| ppp-small-bug | ppp | 6.0 | 10.0 | 60.0% | 0.0 |  |
| shape-clear-small-bug | shape | 5.0 | 8.0 | 62.5% | 0.0 |  |
| shape-large-feature | shape | 5.0 | 13.0 | 38.5% | 0.0 |  |
| shape-public-api-ambiguity | shape | 2.0 | 12.0 | 16.7% | 0.0 |  |
| ship-foundation-first | ship | 13.0 | 13.0 | 100.0% | 0.0 |  |
| ship-review-burden | ship | 12.0 | 12.0 | 100.0% | 0.0 |  |

## Weakest Dimensions

- `Debug Loop`: 0.0/4.0 (0.0%)
- `Blocker Handoff`: 8.0/18.0 (44.4%)
- `Handoff`: 2.0/4.0 (50.0%)
- `Scope`: 6.0/12.0 (50.0%)
- `Preferred Choice`: 11.0/18.0 (61.1%)

## Weakest Cases

- `shape-public-api-ambiguity` (shape): 2.0/12.0 (16.7%)
- `ppp-failing-test` (ppp): 4.0/14.0 (28.6%)
- `shape-large-feature` (shape): 5.0/13.0 (38.5%)
- `ppp-small-bug` (ppp): 6.0/10.0 (60.0%)
- `shape-clear-small-bug` (shape): 5.0/8.0 (62.5%)

## Most Missed Criteria

- `keeps-first-pr-visible` (Scope): missed in 1 case(s)
- `preferred-first-slice-and-route` (Preferred Choice): missed in 1 case(s)
- `route-to-ship-or-decision` (Routing): missed in 1 case(s)
- `blocked-handoff-proof-gap` (Blocker Handoff): missed in 1 case(s)
- `blocked-handoff-resumable-next-step` (Blocker Handoff): missed in 1 case(s)
- `bounded-attempts` (Debug Loop): missed in 1 case(s)
- `one-cause-per-attempt` (Debug Loop): missed in 1 case(s)
- `pr-review-handoff` (Handoff): missed in 1 case(s)
- `preferred-blocker-shape-structure` (Preferred Choice): missed in 1 case(s)
- `preferred-debugging-handoff-structure` (Preferred Choice): missed in 1 case(s)
