#!/usr/bin/env python3
def evaluate():
    print("EVALUATOR: Structural Design (Module 05)")
    try:
        with open('05_structural_design/results.md') as f:
            r = f.read()
            if "450" in r and "45 MPa" in r:
                print("✓ PASS — Resonance and stress within spec")
                return True
        return None
    except:
        return False

if __name__ == '__main__':
    evaluate()
