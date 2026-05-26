#!/usr/bin/env python3
import json

opus = json.loads(open('evals/runs/2026-05-26-opus-4-6/results.json').read())
sonnet = json.loads(open('evals/runs/2026-05-26-sonnet-4-6/results.json').read())

print('=' * 70)
print('PENALTIES TRIGGERED IN OPUS')
print('=' * 70)
penalty_count = 0
for case in opus['cases']:
    for c in case.get('criteria', []):
        if c.get('kind') == 'penalty' and c.get('matched'):
            penalty_count += 1
            print(f"\nPenalty #{penalty_count}:")
            print(f"  Case: {case['id']}")
            print(f"  Criterion: {c['name']}")
            print(f"  Dimension: {c['dimension']}")
            print(f"  Points deducted: -{c['points']}")
            print(f"  Description: {c['description']}")

print(f"\n\nTotal penalties in Opus: {penalty_count}")
print(f"Total penalty points: -2.0\n")

# ppp-proof-trap case analysis
print('=' * 70)
print('PPP-PROOF-TRAP CASE BREAKDOWN (OPUS vs SONNET)')
print('=' * 70)

for case in opus['cases']:
    if case['id'] == 'ppp-proof-trap':
        print("\n--- OPUS (score: 3.0/11.0, 27.3%) ---")
        for c in case.get('criteria', []):
            m = "✓ PASS" if c['matched'] else "✗ MISS"
            print(f"{m}: {c['name']:<35} {c['earned']:+.0f} pts (max {c['points']})")

for case in sonnet['cases']:
    if case['id'] == 'ppp-proof-trap':
        print("\n--- SONNET (score: 11.0/11.0, 100%) ---")
        for c in case.get('criteria', []):
            m = "✓ PASS" if c['matched'] else "✗ MISS"
            print(f"{m}: {c['name']:<35} {c['earned']:+.0f} pts (max {c['points']})")

print("\n" + '=' * 70)
print('OVERALL TALLY')
print('=' * 70)
print("\nOpus:")
print(f"  Reward: 79.0 pts")
print(f"  Penalty: -2.0 pts")
print(f"  Raw net: 77.0 pts")
print(f"  Final: 77.0 / 115.0 = 67.0%")

print("\nSonnet:")
print(f"  Reward: 80.0 pts")
print(f"  Penalty: 0.0 pts")
print(f"  Raw net: 80.0 pts")
print(f"  Final: 80.0 / 115.0 = 69.6%")

print("\nDifference: Sonnet is +2.6 percentage points higher")
print("\nBreakdown:")
print(f"  - Sonnet earns 1 more reward point (80 vs 79)")
print(f"  - Opus is penalized 2 points (vs Sonnet's 0)")
print(f"  - Total swing: 3 points in Sonnet's favor")
