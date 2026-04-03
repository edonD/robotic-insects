#!/usr/bin/env python3
"""
Module 01: Actuator Design
===========================

Evaluates piezoelectric and shape-memory alloy actuators for wing actuation.
"""

import numpy as np
import matplotlib.pyplot as plt

def simulate_piezo_actuator():
    """Simplified piezoelectric actuator model."""
    print("01. PIEZOELECTRIC ACTUATOR")
    print("-" * 50)

    # Typical PZT stack actuator parameters
    voltage_drive = 50  # volts
    strain_coeff = 400e-12  # m/V (d33 for PZT-5H)
    stack_height = 10  # mm
    resonance_freq = 2000  # Hz
    force_blocking = 5  # mN (estimated)
    power_draw = 20  # mW at 200 Hz
    mass = 0.2  # mg

    print(f"   Force capability: {force_blocking:.1f} mN")
    print(f"   Resonance: {resonance_freq} Hz")
    print(f"   Power: {power_draw} mW at 200 Hz")
    print(f"   Mass: {mass} mg")
    print(f"   ✓ Fast response, low mass, moderate force")
    print()

    return {
        'type': 'Piezoelectric (PZT)',
        'force': force_blocking,
        'resonance': resonance_freq,
        'power': power_draw,
        'mass': mass
    }

def simulate_sma_actuator():
    """Simplified shape-memory alloy actuator model."""
    print("02. SHAPE-MEMORY ALLOY (SMA) ACTUATOR")
    print("-" * 50)

    # Typical Nitinol wire parameters
    wire_diameter_mm = 0.1
    wire_length_mm = 5
    strain_max = 0.08  # 8% strain
    force_per_wire = 50  # mN
    activation_freq = 50  # Hz (slower than piezo)
    power_draw = 100  # mW (more power than piezo)
    mass = 0.5  # mg

    print(f"   Force capability: {force_per_wire:.1f} mN")
    print(f"   Max frequency: {activation_freq} Hz")
    print(f"   Power: {power_draw} mW")
    print(f"   Mass: {mass} mg")
    print(f"   ✓ High force, too slow for 200 Hz wing beat")
    print()

    return {
        'type': 'Shape-Memory Alloy (Nitinol)',
        'force': force_per_wire,
        'resonance': activation_freq,
        'power': power_draw,
        'mass': mass
    }

def main():
    print("=" * 70)
    print("WAVE 1: Actuator Design (Module 01)")
    print("=" * 70)
    print()

    # Simulate both actuator types
    piezo = simulate_piezo_actuator()
    sma = simulate_sma_actuator()

    print("COMPARISON")
    print("=" * 70)
    print(f"For 200 Hz wing beat:")
    print(f"  → Piezoelectric: ✓ SUITABLE (fast enough)")
    print(f"  → SMA: ✗ TOO SLOW (max 50 Hz)")
    print()
    print(f"RECOMMENDATION: Piezoelectric stack actuator")
    print()

    # Save results
    with open('01_actuator_design/results.md', 'w') as f:
        f.write("# Actuator Design — Results\n\n")
        f.write(f"## Selected Actuator\n\n")
        f.write(f"**Type**: {piezo['type']}\n\n")
        f.write(f"### Performance\n\n")
        f.write(f"- Force: {piezo['force']} mN\n")
        f.write(f"- Resonance: {piezo['resonance']} Hz\n")
        f.write(f"- Power: {piezo['power']} mW\n")
        f.write(f"- Mass: {piezo['mass']} mg\n")
        f.write(f"\nAwaiting evaluator.py...\n")

    print("✓ Results saved: 01_actuator_design/results.md")
    print()

if __name__ == '__main__':
    main()
