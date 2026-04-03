#!/usr/bin/env python3
"""Module 10: Evaluator — 3D Visualization"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import load_results_json

def evaluate():
    print("=" * 70)
    print("EVALUATOR: 3D Visualization (Module 10)")
    print("=" * 70)
    print()

    results = load_results_json('10_3d_visualization')

    if not results:
        print("✗ ERROR: results.json not found. Run sim.py first.")
        return False

    max_alt = results.get('max_altitude_m', 0)
    hover_time = results.get('hover_duration_s', 0)

    print(f"Max altitude: {max_alt*1000:.1f} mm")
    print(f"Hover duration: {hover_time:.1f} s")
    print()

    if max_alt > 0 and hover_time >= 5.0:
        print("✓ PASS — 3D simulations completed successfully.")
        return True
    else:
        print("✗ Check simulation parameters.")
        return False

if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
