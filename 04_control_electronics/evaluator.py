#!/usr/bin/env python3
def evaluate():
    print("EVALUATOR: Control Electronics (Module 04)")
    try:
        with open('04_control_electronics/results.md') as f:
            if "Cortex" in f.read():
                print("✓ PASS")
                return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
