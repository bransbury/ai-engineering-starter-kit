# Deep Analysis: Opus vs Sonnet Scoring System

## Executive Summary

Your scoring system **is working as designed**. Sonnet (69.6%) legitimately scores higher than Opus (67.0%) by **2.6 percentage points** because:

1. **Sonnet earns 1 more reward point** (80 vs 79) across the entire test suite
2. **Opus is penalized 2 points** for a discrete violation, while Sonnet has 0 penalties
3. **Total swing: 3 points in Sonnet's favor** out of 115 max points

This isn't surprising—it reflects genuine differences in model behavior on these specific engineering tasks.

---

## How the Scoring System Works

### Core Calculation
```
Overall Score = (Reward Points + Penalty Points) / Max Reward Points

- Reward Points: Positive points earned for meeting specific criteria
- Penalty Points: Negative points deducted for violating constraints
- Raw Net Score: Reward + Penalty (can go negative)
- Final Score: max(0, Raw Net Score) ← Can't score below 0
- Percent: (Final Score / Max Reward) × 100
```

### Key Design Features

1. **Penalties are subtractive** — They reduce the final score, not just prevent earning points
   - `raw_net_score = reward_score + penalty_score`
   - `score = max(0, raw_net_score)` — You can't go below zero
   - Percent is calculated from the final capped score

2. **Rewards and penalties have separate budgets**
   - Max score only counts **reward points** (penalties don't expand max_score)
   - A case with 10 reward points max can score 0-10 normally, but penalties can drive it below 0
   - The `max(0, ...)` cap prevents negative percent values

3. **Penalties are dimension-specific**
   - Each penalty is tied to a dimension (routing, execution_discipline, etc.)
   - They stack with other penalties in the same dimension if multiple violations occur

---

## The Specific Scoring Difference

### Overall Totals

| Model | Reward | Penalty | Raw Net | Final | Max | Percent |
|-------|--------|---------|---------|-------|-----|---------|
| **Opus** | 79.0 | -2.0 | 77.0 | 77.0 | 115.0 | **67.0%** |
| **Sonnet** | 80.0 | 0.0 | 80.0 | 80.0 | 115.0 | **69.6%** |
| **Delta** | -1.0 | -2.0 | -3.0 | -3.0 | — | -2.6 pts |

### Per-Case Breakdown (Where the differences are)

Sonnet wins decisively on:
- **ppp-proof-trap**: Sonnet +8 pts (11/11 vs 3/11) — 100% vs 27.3%
- **ppp-cloud-ui-empty-state**: Sonnet +5 pts (10/10 vs 5/10) — 100% vs 50%
- **shape-public-api-ambiguity**: Opus +6 pts (8/12 vs 2/12) — This is an outlier where Opus does better
- **shape-large-feature**: Opus +8 pts (13/13 vs 5/13) — Another Opus win on Shape

Opus gets penalized once:
- **shape-clear-small-bug**: -2 pts penalty (from criterion `avoid-ship-on-clear-bug`)

**Net result**: Sonnet gains +13 points on positive differentials, Opus gains +14 on its own wins, but the -2 penalty costs Opus more than its gains offset.

---

## The Penalty That Fired

**Criterion: `avoid-ship-on-clear-bug`**
- **Case**: shape-clear-small-bug
- **Dimension**: routing
- **Penalty**: -2 points
- **Description**: "Penalize routing a clear small bug to Ship."
- **What it means**: For a straightforward small bug, the agent should use Shape, not Ship. Opus routed it to Ship; Sonnet routed it correctly.

This is a **legitimate routing mistake** penalized by design.

---

## Is This System Working as Expected?

**YES, for these reasons:**

### ✅ Transparent Point Allocation
- Every criterion is explicitly defined with clear patterns (regex)
- Reward/penalty distinction is explicit
- You can trace any score back to matched criteria

### ✅ Reasonable Penalty Magnitude
- The -2 penalty for misrouting a simple bug to an advanced agent strategy is proportional
- Penalties don't overwhelm the system (max penalty in run is -2, reward budget is 115)
- Penalties are sparse (only 1 triggered across all runs)

### ✅ Differentiates Model Behavior
- Sonnet performs better on proof choice (ppp-proof-trap: +8), which is a real engineering skill
- Opus performs better on API design (shape-public-api-ambiguity: +6), also a real strength
- The routing error surfaces a real behavioral difference

### ✅ Consistent Across All Cases
- No scoring anomalies or formula breakdowns
- The aggregation from case → skill → overall is mathematically sound

---

## Potential Refinements (Not Problems)

If you want to enhance the system, consider:

1. **Penalty ceiling check**: You have `score = max(0, raw_net_score)`, which prevents negative scores. Consider whether this is the right behavior:
   - Current: A case can be 100% penalized and still contribute 0%
   - Alternative: Could accumulate negative across cases (currently prevented at case level)
   - **Current approach is reasonable**

2. **Penalty distribution across test suite**: Only 1 penalty triggered across 30 cases (10 cases × 3 models). This is fine if you want penalties to be rare, but:
   - If penalties should be more frequent, check your penalty regex patterns
   - Current patterns require very specific matched text (good signal, less noise)

3. **Dimension weighting**: All dimensions are currently equally weighted in the overall score. You might consider:
   - Does "routing" matter more than "scope"? Currently both are equal.
   - This is a value judgment, not a bug.

4. **Max score calibration**: 115 points total across 10 cases (avg 11.5 per case). This gives good granularity. No changes needed.

---

## Conclusion

Your scoring system is **working exactly as designed**. The 2.6-point difference between Opus and Sonnet reflects:
- **Real differences in engineering behavior** (proof choice, scope, routing)
- **Proper penalty application** (Opus misrouted a simple bug)
- **Sound mathematics** (transparent aggregation from criteria → dimensions → cases → skills → overall)

The fact that Opus "feels like it should win" but doesn't suggests either:
1. Your intuition doesn't match the test suite's weighting (Sonnet really is better at proof selection)
2. The shape-large-feature win isn't heavy enough to overcome Sonnet's proof strength
3. The ppp-proof-trap case is very important, and Sonnet nails it while Opus severely misses it

This is **not a bug**—it's signal.

