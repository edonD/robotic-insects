#!/usr/bin/env python3
"""Module 05: Evaluator — Structural Design"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric


def evaluate():
    print("=" * 70)
    print("EVALUATOR: Structural Design (Module 05)")
    print("=" * 70)
    print()

    results = load_results_json('05_structural_design')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False

    wing_freq = results.get('wing_first_mode_hz', 0)
    body_freq = results.get('body_natural_frequency_hz', 0)
    stress_sf = results.get('wing_stress_safety_factor', 0)

    checks = [
        ('Wing 1st mode frequency', wing_freq, 200.0, '>='),
        ('Body natural frequency', body_freq, 50.0, '>='),
        ('Stress safety factor', stress_sf, 2.0, '>='),
    ]

    all_pass = evaluate_numeric(checks)

    print()
    if all_pass:
        print("OK: PASS — Structure is mechanically sound.")
        return True
    else:
        print("XX: FAIL — Structural issues require redesign.")
        return False


if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
