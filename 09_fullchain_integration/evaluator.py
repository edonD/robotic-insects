#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json

def evaluate():
    print("=" * 70)
    print("EVALUATOR: Full-Chain Integration (Module 09)")
    print("=" * 70)
    print()
    results = load_results_json('09_fullchain_integration')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False
    status = results.get('overall_status', 'FAIL')
    passed = results.get('constraints_passed', 0)
    total = results.get('total_constraints', 8)
    print(f"Constraints: {passed}/{total} passed")
    print(f"Overall: {status}")
    print()
    if status == 'PASS':
        print("OK: PASS — System is fully integrated and feasible.")
        return True
    else:
        print("XX: FAIL — Some constraints not met. See details above.")
        return False

if __name__ == '__main__':
    sys.exit(0 if evaluate() else 1)
