#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric

def evaluate():
    print("=" * 70)
    print("EVALUATOR: Fabrication Plan (Module 08)")
    print("=" * 70)
    print()
    results = load_results_json('08_fabrication_plan')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False
    yield_pct = results.get('overall_yield_percent', 0)
    cost = results.get('prototype_cost_per_unit_usd', 0)
    checks = [('Overall yield', yield_pct, 20.0, '>='), ('Prototype cost per unit', cost, 250.0, '<=')]
    all_pass = evaluate_numeric(checks)
    print()
    if all_pass:
        print("OK: PASS — Manufacturing is economically feasible.")
        return True
    else:
        print("XX: FAIL — Cost or yield needs improvement.")
        return False

if __name__ == '__main__':
    sys.exit(0 if evaluate() else 1)
