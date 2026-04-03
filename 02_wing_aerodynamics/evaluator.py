#!/usr/bin/env python3
"""Module 02: Evaluator — Wing Aerodynamics"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric


def evaluate():
    print("=" * 70)
    print("EVALUATOR: Wing Aerodynamics (Module 02)")
    print("=" * 70)
    print()

    results = load_results_json('02_wing_aerodynamics')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False

    thrust_mn = results.get('thrust_at_design_mN', 0)
    reynolds = results.get('reynolds_number', 0)
    twr = results.get('thrust_to_weight_ratio', 0)

    checks = [
        ('Thrust @ 200 Hz', thrust_mn, 0.001, '>='),
        ('Reynolds number (valid range)', reynolds, 100, '>='),
        ('Thrust-to-weight ratio', twr, 1.5, '>='),
    ]

    all_pass = evaluate_numeric(checks)

    print()
    if all_pass:
        print("OK: PASS — Wing aerodynamics feasible.")
        return True
    else:
        print("XX: FAIL — Review wing specifications.")
        return False


if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
