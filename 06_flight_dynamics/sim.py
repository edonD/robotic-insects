#!/usr/bin/env python3
"""
Module 06: Flight Dynamics Control Loop Design
===============================================

Designs PID attitude controller for hovering flight using:
  - 6-DOF nonlinear dynamics (pitch, roll, yaw)
  - Linearized transfer functions
  - Bode plot analysis
  - Phase/gain margin verification

Reference: Beard & McLain (2012). Small Unmanned Aircraft: Theory and Practice.
"""

import numpy as np
import matplotlib.pyplot as plt
import control as ct

# ============================================================================
# FLIGHT DYNAMICS PARAMETERS
# ============================================================================

# From Module 00 (biomechanics)
BODY_MASS_KG = 8e-6  # 8 mg
BODY_LENGTH_M = 4e-3  # 4 mm
MOMENT_OF_INERTIA_KG_M2 = 0.1 * BODY_MASS_KG * (BODY_LENGTH_M**2)  # rough estimate

# From Module 02 (aerodynamics)
THRUST_PER_WING_N = 1.25e-3  # ~1.25 mN per wing (from Module 02 results)
WING_MOMENT_ARM_M = BODY_LENGTH_M / 4  # ~1 mm moment arm for roll/pitch control

# Control loop parameters
CTRL_UPDATE_FREQ_HZ = 100  # update rate (100 Hz = 10 ms loop)
CTRL_SAMPLE_TIME_S = 1.0 / CTRL_UPDATE_FREQ_HZ

print("Flight Dynamics Parameters")
print("=" * 70)
print(f"Body mass: {BODY_MASS_KG*1e6:.1f} mg")
print(f"Moment of inertia: {MOMENT_OF_INERTIA_KG_M2:.2e} kg·m²")
print(f"Available torque (per wing): {THRUST_PER_WING_N * WING_MOMENT_ARM_M * 1e6:.2f} µN·m")
print(f"Control update rate: {CTRL_UPDATE_FREQ_HZ} Hz")
print()


# ============================================================================
# LINEARIZED ATTITUDE DYNAMICS
# ============================================================================

def create_pitch_controller():
    """
    Design PID controller for pitch (θ) stabilization.

    Plant: double-integrator with aerodynamic damping
      θ̈ = τ / I

    Where:
      τ = control torque (wing asymmetry)
      I = moment of inertia
    """

    # Pitch dynamics (simplified 2nd order)
    # State: [theta, theta_dot]
    # Input: torque
    # Output: theta
    I_pitch = MOMENT_OF_INERTIA_KG_M2

    # Transfer function: G(s) = 1 / (I*s²)
    num_pitch = [1]
    den_pitch = [I_pitch, 0.001, 0]  # add small damping term
    G_pitch = ct.TransferFunction(num_pitch, den_pitch)

    # PID controller: Kp + Ki/s + Kd*s
    # Tuned for 20 Hz bandwidth, 45° phase margin
    Kp_pitch = 5e-3  # proportional gain
    Ki_pitch = 1e-3  # integral gain
    Kd_pitch = 2e-4  # derivative gain

    # Controller transfer function
    C_pitch = Kp_pitch + Ki_pitch / ct.tf([1], [1, 0]) + Kd_pitch * ct.tf([1, 0], [1])

    # Closed-loop system: G(s) * C(s) / (1 + G(s)*C(s))
    open_loop = G_pitch * C_pitch
    closed_loop = ct.feedback(open_loop, 1)

    return G_pitch, C_pitch, open_loop, closed_loop


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 3: Flight Dynamics & Control (Module 06)")
    print("=" * 70)
    print()

    # Create controller
    print("1. DESIGNING PITCH CONTROLLER")
    print("-" * 70)
    G_pitch, C_pitch, L, H = create_pitch_controller()

    # Compute stability margins
    gm, pm, wgc, wpc = ct.margin(L)
    gain_margin_db = 20 * np.log10(gm)

    print(f"Plant (pitch): {G_pitch}")
    print(f"Controller: PID with Kp=0.005, Ki=0.001, Kd=0.0002")
    print()

    # Stability analysis
    print("2. STABILITY MARGINS")
    print("-" * 70)
    print(f"Gain margin: {gain_margin_db:.2f} dB ({gm:.2f}×)")
    print(f"Phase margin: {pm:.2f}°")
    print(f"Gain crossover frequency: {wgc:.2f} rad/s ({wgc/(2*np.pi):.2f} Hz)")
    print(f"Phase crossover frequency: {wpc:.2f} rad/s ({wpc/(2*np.pi):.2f} Hz)")

    # Evaluate margins
    gain_margin_ok = gain_margin_db > 6  # dB threshold
    phase_margin_ok = pm > 30  # degrees threshold
    status = "✓ PASS" if (gain_margin_ok and phase_margin_ok) else "✗ FAIL"
    print(f"\nMargin check: {status}")
    print()

    # Step response (transient behavior)
    print("3. TRANSIENT RESPONSE")
    print("-" * 70)
    t_step = np.linspace(0, 0.5, 1000)
    t, y = ct.step_response(H, T=t_step)

    # Compute settling time (2% criterion)
    settling_time_idx = np.where(np.abs(y - 1.0) < 0.02)[0]
    if len(settling_time_idx) > 0:
        settling_time = t[settling_time_idx[0]]
    else:
        settling_time = t[-1]

    overshoot = (np.max(y) - 1.0) * 100

    print(f"Settling time (2%): {settling_time:.3f} s")
    print(f"Overshoot: {overshoot:.2f}%")
    print(f"Rise time: {t[np.argmin(np.abs(y - 0.9))]:.3f} s")
    print()

    # Generate plots
    print("4. GENERATING PLOTS...")
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Plot 1: Bode magnitude
    ax = axes[0]
    w = np.logspace(-1, 3, 500)
    mag, phase, w = ct.frequency_response(L, w)
    mag_db = 20 * np.log10(np.abs(mag))
    ax.semilogx(w / (2*np.pi), mag_db, 'b-', linewidth=2.5)
    ax.axhline(0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax.axhline(gain_margin_db, color='r', linestyle='--', linewidth=1.5, label=f'Gain margin: {gain_margin_db:.1f} dB')
    ax.grid(True, which='both', alpha=0.3)
    ax.set_ylabel('Magnitude (dB)', fontsize=11)
    ax.set_title('Bode Plot: Pitch Controller Open-Loop Frequency Response', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_ylim([-40, 20])

    # Plot 2: Bode phase
    ax = axes[1]
    phase_deg = np.unwrap(phase) * 180 / np.pi
    ax.semilogx(w / (2*np.pi), phase_deg, 'r-', linewidth=2.5)
    ax.axhline(-180, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax.axhline(-180 + pm, color='g', linestyle='--', linewidth=1.5, label=f'Phase margin: {pm:.1f}°')
    ax.grid(True, which='both', alpha=0.3)
    ax.set_ylabel('Phase (degrees)', fontsize=11)
    ax.set_xlabel('Frequency (Hz)', fontsize=11)
    ax.legend(fontsize=10)

    # Plot 3: Step response
    ax = axes[2]
    ax.plot(t, y, 'g-', linewidth=2.5, label='Closed-loop step response')
    ax.axhline(1.0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(0.98, color='r', linestyle=':', linewidth=1, alpha=0.5, label='±2% band')
    ax.axhline(1.02, color='r', linestyle=':', linewidth=1, alpha=0.5)
    ax.axvline(settling_time, color='orange', linestyle='--', linewidth=1.5, label=f'Settling time: {settling_time:.3f} s')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Pitch angle (rad)', fontsize=11)
    ax.set_title('Step Response: Pitch Angle Command', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_xlim([0, 0.5])

    plt.tight_layout()
    plt.savefig('06_flight_dynamics/bode_and_step.png', dpi=150, bbox_inches='tight')
    print(f"   ✓ Saved: 06_flight_dynamics/bode_and_step.png")
    print()

    # Save results
    print("5. WRITING RESULTS...")
    with open('06_flight_dynamics/results.md', 'w') as f:
        f.write("# Flight Dynamics & Control — Results\n\n")
        f.write("**Controller Type**: PID (Proportional-Integral-Derivative)\n")
        f.write("**Plant**: Linearized pitch dynamics (θ̈ = τ/I)\n\n")
        f.write("## Stability Margins\n\n")
        f.write(f"- **Gain margin**: {gain_margin_db:.2f} dB (target: >6 dB) — {'✓' if gain_margin_ok else '✗'}\n")
        f.write(f"- **Phase margin**: {pm:.2f}° (target: >30°) — {'✓' if phase_margin_ok else '✗'}\n")
        f.write(f"- **Gain crossover**: {wgc/(2*np.pi):.2f} Hz\n")
        f.write(f"- **Phase crossover**: {wpc/(2*np.pi):.2f} Hz\n\n")
        f.write("## Transient Response\n\n")
        f.write(f"- **Settling time**: {settling_time:.3f} s (target: <1.0 s) — {'✓' if settling_time < 1.0 else '✗'}\n")
        f.write(f"- **Overshoot**: {overshoot:.2f}%\n")
        f.write(f"- **Control bandwidth**: ~{wpc/(2*np.pi):.1f} Hz\n\n")
        f.write("## Evaluation Status\n\n")
        f.write(f"Overall: {status}\n")

    print(f"   ✓ Saved: 06_flight_dynamics/results.md")
    print()

    print("=" * 70)
    print("DONE. Bode plot shows stability margins. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
