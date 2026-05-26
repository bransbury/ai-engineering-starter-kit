# Skill Eval Scoreboard

This table compares scored eval runs across models and agents. Use runs from the same case set and skill commit when you want a fair comparison.

| Run ID | Provider | Model | Agent | Cases | Overall | Shape | Ship | PPP | PPP Cloud |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-26-gpt-5-4 | openai | gpt-5-4 | vscode | 10/10 | 95.7% | 90.9% | 100.0% | 94.3% | 100.0% |
| 2026-05-26-opus-4-6 | anthropic | opus-4-6 | vscode | 10/10 | 67.0% | 72.7% | 100.0% | 31.4% | 77.3% |
| 2026-05-26-sonnet-4-6 | anthropic | sonnet-4-6 | vscode | 10/10 | 69.6% | 36.4% | 100.0% | 60.0% | 100.0% |

## Dimension Matrix

| Run ID | Model | Agent | Risk Routing | Blocker Handoff | Preferred Choice | Execution Discipline | Scope | Pattern Reuse | Proof | Handoff | Diagnosis | Debug Loop | Inspection | Routing | Interaction | Dependency Planning | Wave Planning | Reviewability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-26-gpt-5-4 | gpt-5-4 | vscode | 100.0% | 100.0% | 100.0% | 0.0% | 75.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| 2026-05-26-opus-4-6 | opus-4-6 | vscode | 100.0% | 66.7% | 61.1% | 0.0% | 33.3% | 100.0% | 78.9% | 0.0% | 0.0% | 0.0% | 66.7% | 83.3% | 0.0% | 100.0% | 100.0% | 100.0% |
| 2026-05-26-sonnet-4-6 | sonnet-4-6 | vscode | 75.0% | 44.4% | 61.1% | 0.0% | 50.0% | 100.0% | 94.7% | 50.0% | 100.0% | 0.0% | 100.0% | 75.0% | 0.0% | 100.0% | 100.0% | 100.0% |

## Pairwise Comparison

### 2026-05-26-gpt-5-4 vs 2026-05-26-opus-4-6

- `2026-05-26-gpt-5-4`: gpt-5-4 (vscode)
- `2026-05-26-opus-4-6`: opus-4-6 (vscode)
- Fingerprint match: no. Treat this as a directional comparison only.
- Overall winner: `2026-05-26-gpt-5-4` by +28.7 pts.

#### Skill Edges

- `2026-05-26-gpt-5-4` leads on: `PPP` (+62.9 pts), `PPP Cloud` (+22.7 pts), `Shape` (+18.2 pts).
- `2026-05-26-opus-4-6` leads on: none.
- Tied skills: `Ship`.

#### Dimension Edges

- `2026-05-26-gpt-5-4` leads on: `Debug Loop` (+100.0 pts), `Diagnosis` (+100.0 pts), `Handoff` (+100.0 pts), `Scope` (+41.7 pts), `Preferred Choice` (+38.9 pts), `Blocker Handoff` (+33.3 pts), `Inspection` (+33.3 pts), `Proof` (+21.1 pts), `Routing` (+16.7 pts).
- `2026-05-26-opus-4-6` leads on: none.
- Tied dimensions: `Dependency Planning`, `Execution Discipline`, `Interaction`, `Pattern Reuse`, `Reviewability`, `Risk Routing`, `Wave Planning`.

#### Top Separating Cases

- `2026-05-26-gpt-5-4` strongest cases: `ppp-failing-test` (+85.7 pts), `ppp-proof-trap` (+54.5 pts), `ppp-cloud-ui-empty-state` (+50.0 pts), `ppp-small-bug` (+40.0 pts), `shape-public-api-ambiguity` (+33.3 pts).
- `2026-05-26-opus-4-6` strongest cases: none.
- Tied cases: 4 of 10.

### 2026-05-26-gpt-5-4 vs 2026-05-26-sonnet-4-6

- `2026-05-26-gpt-5-4`: gpt-5-4 (vscode)
- `2026-05-26-sonnet-4-6`: sonnet-4-6 (vscode)
- Fingerprint match: yes
- Overall winner: `2026-05-26-gpt-5-4` by +26.1 pts.

#### Skill Edges

- `2026-05-26-gpt-5-4` leads on: `Shape` (+54.5 pts), `PPP` (+34.3 pts).
- `2026-05-26-sonnet-4-6` leads on: none.
- Tied skills: `PPP Cloud`, `Ship`.

#### Dimension Edges

- `2026-05-26-gpt-5-4` leads on: `Debug Loop` (+100.0 pts), `Blocker Handoff` (+55.6 pts), `Handoff` (+50.0 pts), `Preferred Choice` (+38.9 pts), `Risk Routing` (+25.0 pts), `Routing` (+25.0 pts), `Scope` (+25.0 pts), `Proof` (+5.3 pts).
- `2026-05-26-sonnet-4-6` leads on: none.
- Tied dimensions: `Dependency Planning`, `Diagnosis`, `Execution Discipline`, `Inspection`, `Interaction`, `Pattern Reuse`, `Reviewability`, `Wave Planning`.

#### Top Separating Cases

- `2026-05-26-gpt-5-4` strongest cases: `shape-public-api-ambiguity` (+83.3 pts), `ppp-failing-test` (+71.4 pts), `shape-large-feature` (+61.5 pts), `ppp-small-bug` (+40.0 pts).
- `2026-05-26-sonnet-4-6` strongest cases: `ppp-proof-trap` (+18.2 pts).
- Tied cases: 5 of 10.

### 2026-05-26-opus-4-6 vs 2026-05-26-sonnet-4-6

- `2026-05-26-opus-4-6`: opus-4-6 (vscode)
- `2026-05-26-sonnet-4-6`: sonnet-4-6 (vscode)
- Fingerprint match: no. Treat this as a directional comparison only.
- Overall winner: `2026-05-26-sonnet-4-6` by +2.6 pts.

#### Skill Edges

- `2026-05-26-opus-4-6` leads on: `Shape` (+36.3 pts).
- `2026-05-26-sonnet-4-6` leads on: `PPP` (+28.6 pts), `PPP Cloud` (+22.7 pts).
- Tied skills: `Ship`.

#### Dimension Edges

- `2026-05-26-opus-4-6` leads on: `Risk Routing` (+25.0 pts), `Blocker Handoff` (+22.3 pts), `Routing` (+8.3 pts).
- `2026-05-26-sonnet-4-6` leads on: `Diagnosis` (+100.0 pts), `Handoff` (+50.0 pts), `Inspection` (+33.3 pts), `Scope` (+16.7 pts), `Proof` (+15.8 pts).
- Tied dimensions: `Debug Loop`, `Dependency Planning`, `Execution Discipline`, `Interaction`, `Pattern Reuse`, `Preferred Choice`, `Reviewability`, `Wave Planning`.

#### Top Separating Cases

- `2026-05-26-opus-4-6` strongest cases: `shape-large-feature` (+61.5 pts), `shape-public-api-ambiguity` (+50.0 pts).
- `2026-05-26-sonnet-4-6` strongest cases: `ppp-proof-trap` (+72.7 pts), `ppp-cloud-ui-empty-state` (+50.0 pts), `shape-clear-small-bug` (+25.0 pts), `ppp-failing-test` (+14.3 pts).
- Tied cases: 4 of 10.

## Saturation Analysis

This section analyzes only comparable run cohorts that share the same fingerprint. A metric is `high-signal` when it clearly separates runs, `medium-signal` when it shows some spread, and `saturated` when it no longer provides meaningful separation.

### Fingerprint Cohort `c9529c146440` (1 runs)

Need at least two runs in the same fingerprint cohort.

### Fingerprint Cohort `db94cc75d3ed` (2 runs)

- `skills`: 2 high-signal, 0 medium-signal, 2 saturated.
- `dimensions`: 7 high-signal, 0 medium-signal, 9 saturated.
- `cases`: 4 high-signal, 1 medium-signal, 5 saturated.
- `criteria`: 17 high-signal, 0 medium-signal, 52 saturated.

#### Skills

| Metric | Signal | Spread | Full Credit | Avg | Notes |
| --- | --- | --- | --- | --- | --- |
| `Shape` | high-signal | 54.5 pts | 0/2 (0.0%) | 63.7% | Clear separation across runs with 54.5 pts of spread. |
| `PPP` | high-signal | 34.3 pts | 0/2 (0.0%) | 77.2% | Clear separation across runs with 34.3 pts of spread. |
| `PPP Cloud` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Ship` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |

#### Dimensions

| Metric | Signal | Spread | Full Credit | Avg | Notes |
| --- | --- | --- | --- | --- | --- |
| `Debug Loop` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `Blocker Handoff` | high-signal | 55.6 pts | 1/2 (50.0%) | 72.2% | Clear separation across runs with 55.6 pts of spread. |
| `Handoff` | high-signal | 50.0 pts | 1/2 (50.0%) | 75.0% | Clear separation across runs with 50.0 pts of spread. |
| `Preferred Choice` | high-signal | 38.9 pts | 1/2 (50.0%) | 80.5% | Clear separation across runs with 38.9 pts of spread. |
| `Risk Routing` | high-signal | 25.0 pts | 1/2 (50.0%) | 87.5% | Clear separation across runs with 25.0 pts of spread. |
| `Routing` | high-signal | 25.0 pts | 1/2 (50.0%) | 87.5% | Clear separation across runs with 25.0 pts of spread. |
| `Scope` | high-signal | 25.0 pts | 0/2 (0.0%) | 62.5% | Clear separation across runs with 25.0 pts of spread. |
| `Proof` | saturated | 5.3 pts | 1/2 (50.0%) | 97.3% | Low separation only (5.3 pts spread). |
| `Dependency Planning` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Diagnosis` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Execution Discipline` | saturated | 0.0 pts | 0/2 (0.0%) | 0.0% | No separating power. All comparable runs clustered at 0.0%. |
| `Inspection` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Interaction` | saturated | 0.0 pts | 0/2 (0.0%) | 0.0% | No separating power. All comparable runs clustered at 0.0%. |
| `Pattern Reuse` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Reviewability` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `Wave Planning` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |

#### Cases

| Metric | Signal | Spread | Full Credit | Avg | Notes |
| --- | --- | --- | --- | --- | --- |
| `shape-public-api-ambiguity` | high-signal | 83.3 pts | 1/2 (50.0%) | 58.4% | Clear separation across runs with 83.3 pts of spread. |
| `ppp-failing-test` | high-signal | 71.4 pts | 1/2 (50.0%) | 64.3% | Clear separation across runs with 71.4 pts of spread. |
| `shape-large-feature` | high-signal | 61.5 pts | 1/2 (50.0%) | 69.2% | Clear separation across runs with 61.5 pts of spread. |
| `ppp-small-bug` | high-signal | 40.0 pts | 1/2 (50.0%) | 80.0% | Clear separation across runs with 40.0 pts of spread. |
| `ppp-proof-trap` | medium-signal | 18.2 pts | 1/2 (50.0%) | 90.9% | Some separation across runs with 18.2 pts of spread. |
| `ppp-cloud-auth-unclear` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `shape-clear-small-bug` | saturated | 0.0 pts | 0/2 (0.0%) | 62.5% | No separating power. All comparable runs clustered at 62.5%. |
| `ship-foundation-first` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ship-review-burden` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |

#### Criteria

- Top separating criteria:

| Metric | Signal | Spread | Full Credit | Avg | Notes |
| --- | --- | --- | --- | --- | --- |
| `ppp-failing-test / blocked-handoff-proof-gap` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-failing-test / blocked-handoff-resumable-next-step` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-failing-test / bounded-attempts` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-failing-test / one-cause-per-attempt` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-failing-test / preferred-debugging-handoff-structure` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-proof-trap / no-full-suite-as-main-proof` | high-signal | 100.0 pts | 0/2 (0.0%) | -50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-small-bug / pr-review-handoff` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-small-bug / small-safe-scope` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `ppp-small-bug / state-proof-before-patch` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `shape-large-feature / preferred-first-slice-and-route` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `shape-large-feature / route-to-ship-or-decision` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |
| `shape-large-feature / specific-acceptance-criteria` | high-signal | 100.0 pts | 1/2 (50.0%) | 50.0% | Clear separation across runs with 100.0 pts of spread. |

- Saturated criteria:

| Metric | Signal | Spread | Full Credit | Avg | Notes |
| --- | --- | --- | --- | --- | --- |
| `ppp-cloud-auth-unclear / actionable-next-step` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-auth-unclear / explains-why-not-safe-autonomously` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-auth-unclear / no-guessing-through-guardrails` | saturated | 0.0 pts | 0/2 (0.0%) | 0.0% | No separating power. All comparable runs clustered at 0.0%. |
| `ppp-cloud-auth-unclear / preferred-blocker-choice` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-auth-unclear / stops-for-auth-ambiguity` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-auth-unclear / stops-for-public-api-ambiguity` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state / component-proof-path` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state / draft-pr-or-blocker-framing` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state / preserve-loading-and-error-behaviour` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state / reuse-empty-state-pattern` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-cloud-ui-empty-state / single-bounded-task` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |
| `ppp-failing-test / classify-failure` | saturated | 0.0 pts | 2/2 (100.0%) | 100.0% | All comparable runs hit full credit. |

## Case Matrix

| Run ID | Model | Agent | ppp-cloud-auth-unclear | ppp-cloud-ui-empty-state | ppp-failing-test | ppp-proof-trap | ppp-small-bug | shape-clear-small-bug | shape-large-feature | shape-public-api-ambiguity | ship-foundation-first | ship-review-burden |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-26-gpt-5-4 | gpt-5-4 | vscode | 12.0/12.0 | 10.0/10.0 | 14.0/14.0 | 9.0/11.0 | 10.0/10.0 | 5.0/8.0 | 13.0/13.0 | 12.0/12.0 | 13.0/13.0 | 12.0/12.0 |
| 2026-05-26-opus-4-6 | opus-4-6 | vscode | 12.0/12.0 | 5.0/10.0 | 2.0/14.0 | 3.0/11.0 | 6.0/10.0 | 3.0/8.0 | 13.0/13.0 | 8.0/12.0 | 13.0/13.0 | 12.0/12.0 |
| 2026-05-26-sonnet-4-6 | sonnet-4-6 | vscode | 12.0/12.0 | 10.0/10.0 | 4.0/14.0 | 11.0/11.0 | 6.0/10.0 | 5.0/8.0 | 5.0/13.0 | 2.0/12.0 | 13.0/13.0 | 12.0/12.0 |

## Notes

- Use a fresh session per case to reduce context leakage.
- Keep model, tool environment, and exposed sampling settings fixed within a run.
- Exact identical outputs are not guaranteed by most providers; compare scores and drift, not just raw text.
- Compare runs only when the fingerprint matches, or treat differences as case-set/skill-set changes rather than pure model deltas.
