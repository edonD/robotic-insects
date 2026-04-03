#!/usr/bin/env python3
"""
Master Evaluator — Robotic Insects Project
===========================================

Runs all module evaluators in order and reports go/no-go status.
"""

import subprocess
import sys

def run_evaluator(module_name):
    """Run an evaluator and return result (True=PASS, False=FAIL, None=UNKNOWN)"""
    try:
        result = subprocess.run(
            [sys.executable, f"{module_name}/evaluator.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Look for keywords in output
        output = result.stdout.lower() + result.stderr.lower()
        if "pass" in output:
            return True
        elif "fail" in output:
            return False
        else:
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    print("=" * 70)
    print("ROBOTIC INSECTS — MASTER EVALUATOR")
    print("=" * 70)
    print()

    results = {}

    # WAVE 1
    print("WAVE 1: Foundations (Parallel)")
    print("-" * 70)
    wave1_modules = [
        "00_insect_biomechanics",
        "01_actuator_design"
    ]
    for mod in wave1_modules:
        print(f"\nRunning {mod}/evaluator.py...", end=" ")
        result = run_evaluator(mod)
        results[mod] = result
        if result is True:
            print("OK: PASS")
        elif result is False:
            print("XX: FAIL")
        else:
            print("??: UNKNOWN (run sim.py first)")

    # Check Wave 1 before proceeding
    wave1_pass = all(results[m] is True for m in wave1_modules if results[m] is not None)
    if not wave1_pass:
        print("\n" + "=" * 70)
        print("WAVE 1 NOT READY — Fix failing modules before Wave 2")
        print("=" * 70)
        return False

    # WAVE 2
    print("\n\nWAVE 2: Subsystems (Parallel, after Wave 1)")
    print("-" * 70)
    wave2_modules = [
        "02_wing_aerodynamics",
        "03_power_management",
        "04_control_electronics",
        "05_structural_design"
    ]
    for mod in wave2_modules:
        print(f"\nRunning {mod}/evaluator.py...", end=" ")
        result = run_evaluator(mod)
        results[mod] = result
        if result is True:
            print("OK: PASS")
        elif result is False:
            print("XX: FAIL")
        else:
            print("??: UNKNOWN (run sim.py first)")

    # WAVE 3
    print("\n\nWAVE 3: Integration (after Wave 2)")
    print("-" * 70)
    wave3_modules = [
        "06_flight_dynamics",
        "07_swarm_coordination",
        "10_3d_visualization"
    ]
    for mod in wave3_modules:
        print(f"\nRunning {mod}/evaluator.py...", end=" ")
        result = run_evaluator(mod)
        results[mod] = result
        if result is True:
            print("OK: PASS")
        elif result is False:
            print("XX: FAIL")
        else:
            print("??: UNKNOWN (run sim.py first)")

    # WAVE 4
    print("\n\nWAVE 4: Manufacturing & Validation (after Wave 3)")
    print("-" * 70)
    wave4_modules = [
        "08_fabrication_plan",
        "09_fullchain_integration"
    ]
    for mod in wave4_modules:
        print(f"\nRunning {mod}/evaluator.py...", end=" ")
        result = run_evaluator(mod)
        results[mod] = result
        if result is True:
            print("OK: PASS")
        elif result is False:
            print("XX: FAIL")
        else:
            print("??: UNKNOWN (run sim.py first)")

    # SUMMARY
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print()

    all_modules = wave1_modules + wave2_modules + wave3_modules + wave4_modules
    passed = sum(1 for m in all_modules if results.get(m) is True)
    failed = sum(1 for m in all_modules if results.get(m) is False)
    unknown = sum(1 for m in all_modules if results.get(m) is None)

    print(f"Results: {passed} PASS, {failed} FAIL, {unknown} UNKNOWN / {len(all_modules)} total")
    print()

    if failed > 0:
        print("XX: PROJECT STATUS: NOT READY")
        print("  Fix failing modules and re-run")
        return False
    elif unknown > 0:
        print("??: PROJECT STATUS: INCOMPLETE")
        print("  Run sim.py in all modules first")
        return None
    else:
        print("OK: PROJECT STATUS: GO")
        print()
        print("All specifications met! Proceed to Phase 2:")
        print("  - design/spec_sheet.md")
        print("  - design/fabrication_traveler.md")
        print("  - design/mems_layout/ (generate GDS-II)")
        print("  - design/bom.md")
        print("  - design/test_protocol.md")
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
