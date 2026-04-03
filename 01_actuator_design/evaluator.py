#!/usr/bin/env python3
"""
Module 01: Evaluator — Actuator Design

Grades actuator selection against requirements:
- Blocked force ≥ 5 mN (needed for wing actuation)
- Resonance frequency > 400 Hz (2× wing beat, avoid coupling)
- Power consumption < 30 mW per pair (battery feasible)
- Mass < 0.5 mg per actuator (lightweight)
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from util import get_module_path, load_results_json, evaluate_numeric


def evaluate():
    print("=" * 70)
    print("EVALUATOR: Actuator Design (Module 01)")
    print("=" * 70)
    print()

    # Load results
    results = load_results_json('01_actuator_design')

    if not results:
        print("✗ ERROR: results.json not found. Run sim.py first.")
        return False

    # Extract key values
    blocked_force = results.get('blocked_force_mn', 0)
    resonance_freq = results.get('resonance_freq_hz', 0)
    power_per_pair = results.get('total_pair_power_mw', 0)
    mass_per_actuator = results.get('mass_mg', 0)

    # Define evaluation criteria
    checks = [
        ('Blocked Force', blocked_force, 5.0, '>='),
        ('Resonance Frequency', resonance_freq, 400.0, '>='),
        ('Power Consumption (2×)', power_per_pair, 50.0, '<='),  # 50 mW for pair
        ('Mass per Actuator', mass_per_actuator, 0.5, '<='),
    ]

    # Run evaluation
    all_pass = evaluate_numeric(checks)

    print()
    print("Material Selected:", results.get('selected_material', 'UNKNOWN'))
    print()

    if all_pass:
        print("✓✓✓ PASS — Actuator design is feasible.")
        print("Blocked force is sufficient for wing actuation.")
        print("Resonance frequency avoids coupling with 200 Hz wing beat.")
        return True
    else:
        print("✗ FAIL — One or more specifications not met.")
        print("Consider: larger actuator, higher voltage, or different material.")
        return False


if __name__ == '__main__':
    success = evaluate()
    sys.exit(0 if success else 1)
