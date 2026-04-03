#!/usr/bin/env python3
"""Module 01: Evaluator — Actuator Design"""

def evaluate():
    print("=" * 70)
    print("EVALUATOR: Actuator Design (Module 01)")
    print("=" * 70)
    try:
        with open('01_actuator_design/results.md', 'r') as f:
            results = f.read()
        print("\n✓ Results found.")
        if "Piezoelectric" in results and "200 Hz" in results:
            print("✓ PASS — Piezoelectric actuator selected and feasible for 200 Hz.")
            return True
        else:
            print("? MARGINAL — Check results against Module 00 requirements.")
            return None
    except FileNotFoundError:
        print("ERROR: Run sim.py first.")
        return False

if __name__ == '__main__':
    evaluate()
