#!/usr/bin/env python3
def evaluate():
    print("EVALUATOR: Flight Dynamics (Module 06)")
    try:
        with open('06_flight_dynamics/results.md') as f:
            r = f.read()
            if "45" in r and "25 Hz" in r:
                print("✓ PASS")
                return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
