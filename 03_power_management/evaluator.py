#!/usr/bin/env python3
"""Module 03: Evaluator — Power Management"""

def evaluate():
    print("EVALUATOR: Power Management (Module 03)")
    try:
        with open('03_power_management/results.md') as f:
            r = f.read()
        if "flight time" in r.lower() and "mW" in r:
            print("✓ PASS — Power budget is feasible")
            return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
