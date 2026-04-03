#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric

def evaluate():
    print("=" * 70)
    print("EVALUATOR: Flight Dynamics (Module 06)")
    print("=" * 70)
    print()
    results = load_results_json('06_flight_dynamics')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False
    gain = results.get('gain_margin_db', 0)
    phase = results.get('phase_margin_deg', 0)
    settling = results.get('settling_time_s', 0)
    checks = [('Gain margin', gain, 6.0, '>='), ('Phase margin', phase, 30.0, '>='), ('Settling time', settling, 1.0, '<=')]
    all_pass = evaluate_numeric(checks)
    print()
    if all_pass:
        print("OK: PASS — Flight control is stable.")
        return True
    else:
        print("XX: FAIL — Control loop needs retuning.")
        return False

if __name__ == '__main__':
    sys.exit(0 if evaluate() else 1)
