#!/usr/bin/env python3
def evaluate():
    print("EVALUATOR: Fabrication Plan (Module 08)")
    try:
        with open('08_fabrication_plan/process_flow.md') as f:
            if "MEMS" in f.read() and "yield" in f.read().lower():
                print("✓ PASS")
                return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
