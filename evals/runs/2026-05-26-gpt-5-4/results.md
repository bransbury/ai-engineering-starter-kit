# Skill Eval Result

- Run ID: `2026-05-26-gpt-5-4`
- Model: `openai/gpt-5-4`
- Agent: `vscode`
- Commit: `2b02289cfb29cf0cec60c219cecf35271271f9a7`
- Total: **110.0/115.0 (95.7%)**
- Reward score: `112.0`; penalties: `-2.0`

## Per Skill

| Skill | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| ppp | 33.0 | 35.0 | 94.3% | -2.0 |
| ppp-cloud | 22.0 | 22.0 | 100.0% | 0.0 |
| shape | 30.0 | 33.0 | 90.9% | 0.0 |
| ship | 25.0 | 25.0 | 100.0% | 0.0 |

## Dimension Breakdown

| Dimension | Score | Max | Percent | Penalties |
|---|---:|---:|---:|---:|
| Execution Discipline | 0.0 | 0.0 | 0.0% | -2.0 |
| Interaction | 0.0 | 0.0 | 0.0% | 0.0 |
| Scope | 9.0 | 12.0 | 75.0% | 0.0 |
| Blocker Handoff | 18.0 | 18.0 | 100.0% | 0.0 |
| Debug Loop | 4.0 | 4.0 | 100.0% | 0.0 |
| Dependency Planning | 2.0 | 2.0 | 100.0% | 0.0 |
| Diagnosis | 2.0 | 2.0 | 100.0% | 0.0 |
| Handoff | 4.0 | 4.0 | 100.0% | 0.0 |
| Inspection | 3.0 | 3.0 | 100.0% | 0.0 |
| Pattern Reuse | 2.0 | 2.0 | 100.0% | 0.0 |
| Preferred Choice | 18.0 | 18.0 | 100.0% | 0.0 |
| Proof | 19.0 | 19.0 | 100.0% | 0.0 |
| Reviewability | 7.0 | 7.0 | 100.0% | 0.0 |
| Risk Routing | 8.0 | 8.0 | 100.0% | 0.0 |
| Routing | 12.0 | 12.0 | 100.0% | 0.0 |
| Wave Planning | 4.0 | 4.0 | 100.0% | 0.0 |

## Cases

| Case | Skill | Score | Max | Percent | Penalties | Notes |
|---|---|---:|---:|---:|---:|---|
| ppp-cloud-auth-unclear | ppp-cloud | 12.0 | 12.0 | 100.0% | 0.0 |  |
| ppp-cloud-ui-empty-state | ppp-cloud | 10.0 | 10.0 | 100.0% | 0.0 |  |
| ppp-failing-test | ppp | 14.0 | 14.0 | 100.0% | 0.0 |  |
| ppp-proof-trap | ppp | 9.0 | 11.0 | 81.8% | -2.0 |  |
| ppp-small-bug | ppp | 10.0 | 10.0 | 100.0% | 0.0 |  |
| shape-clear-small-bug | shape | 5.0 | 8.0 | 62.5% | 0.0 |  |
| shape-large-feature | shape | 13.0 | 13.0 | 100.0% | 0.0 |  |
| shape-public-api-ambiguity | shape | 12.0 | 12.0 | 100.0% | 0.0 |  |
| ship-foundation-first | ship | 13.0 | 13.0 | 100.0% | 0.0 |  |
| ship-review-burden | ship | 12.0 | 12.0 | 100.0% | 0.0 |  |

## Weakest Dimensions

- `Scope`: 9.0/12.0 (75.0%)
- `Pattern Reuse`: 2.0/2.0 (100.0%)
- `Diagnosis`: 2.0/2.0 (100.0%)
- `Dependency Planning`: 2.0/2.0 (100.0%)
- `Inspection`: 3.0/3.0 (100.0%)

## Weakest Cases

- `shape-clear-small-bug` (shape): 5.0/8.0 (62.5%)
- `ppp-proof-trap` (ppp): 9.0/11.0 (81.8%)
- `ppp-cloud-ui-empty-state` (ppp-cloud): 10.0/10.0 (100.0%)
- `ppp-small-bug` (ppp): 10.0/10.0 (100.0%)
- `ppp-cloud-auth-unclear` (ppp-cloud): 12.0/12.0 (100.0%)

## Most Missed Criteria

- `keeps-first-pr-visible` (Scope): missed in 1 case(s)

## Most Triggered Penalties

- `no-full-suite-as-main-proof` (Execution Discipline): triggered in 1 case(s)
