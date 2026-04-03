#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json, evaluate_numeric

def evaluate():
    print("=" * 70)
    print("EVALUATOR: Swarm Coordination (Module 07)")
    print("=" * 70)
    print()
    results = load_results_json('07_swarm_coordination')
    if not results:
        print("ERROR: results.json not found. Run sim.py first.")
        return False
    collision_rate = results.get('collision_rate_per_step', 0)
    formation = results.get('final_formation_quality_m', 0)
    checks = [('Collision rate', collision_rate, 0.1, '<='), ('Formation quality', formation, 2.0, '<=')]
    all_pass = evaluate_numeric(checks)
    print()
    if all_pass:
        print("OK: PASS — Swarm cohesion is good.")
        return True
    else:
        print("XX: FAIL — Collision avoidance needs improvement.")
        return False

if __name__ == '__main__':
    sys.exit(0 if evaluate() else 1)
