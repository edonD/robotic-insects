#!/usr/bin/env python3
"""Module 04: Evaluator — Control Electronics"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric


def evaluate():
    print("=" * 70)
    print("EVALUATOR: Control Electronics (Module 04)")
    print("=" * 70)
    print()

    results = load_results_json('04_control_electronics')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False

    control_freq = results.get('control_frequency_hz', 0)
    adc_enob = results.get('adc_enob_bits', 0)
    latency = results.get('total_latency_ms', 0)

    checks = [
        ('Control frequency', control_freq, 50.0, '>='),
        ('ADC ENOB', adc_enob, 6.0, '>='),
        ('Total latency', latency, 20.0, '<='),
    ]

    all_pass = evaluate_numeric(checks)

    print()
    if all_pass:
        print("OK: PASS — Control system is adequate.")
        return True
    else:
        print("XX: FAIL — Control loop may be too slow or noisy.")
        return False


if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
