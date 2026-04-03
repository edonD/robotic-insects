#!/usr/bin/env python3
"""Module 03: Evaluator — Power Management"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric


def evaluate():
    print("=" * 70)
    print("EVALUATOR: Power Management (Module 03)")
    print("=" * 70)
    print()

    results = load_results_json('03_power_management')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False

    flight_time = results.get('flight_time_minutes', 0)
    total_power = results.get('total_power_mw', 0)

    checks = [
        ('Flight time', flight_time, 4.0, '>='),
        ('Total power', total_power, 100.0, '<='),
    ]

    all_pass = evaluate_numeric(checks)

    print()
    if all_pass:
        print("OK: PASS — Power budget is feasible.")
        return True
    else:
        print("XX: FAIL — Review battery or power consumption.")
        return False


if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
