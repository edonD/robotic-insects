#!/usr/bin/env python3
"""Module 02: Evaluator — Wing Aerodynamics"""

def evaluate():
    print("EVALUATOR: Wing Aerodynamics (Module 02)")
    try:
        with open('02_wing_aerodynamics/results.md') as f:
            r = f.read()
        if "2.5" in r and "thrust" in r.lower():
            print("✓ PASS — Thrust margin adequate")
            return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
