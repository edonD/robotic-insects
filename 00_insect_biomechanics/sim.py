#!/usr/bin/env python3
"""
Module 00: Insect Biomechanics Simulation
==========================================

Simulates the kinematics, muscle activation, and dynamic properties of a target insect.
This is the foundation for all downstream modules (aerodynamics, actuators, control).

References:
  - Dickinson et al. (2000). Active wing kinematics in Drosophila.
  - Fry et al. (2005). Context-dependent flight behavior.
  - Fox & Lehmann (2004). Insect flight control.

Usage:
  python sim.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================================
# USER INPUTS — Edit these based on your target insect
# ============================================================================

INSECT = "Drosophila_melanogaster"
BODY_MASS_MG = 1.0  # milligrams
WING_SPAN_MM = 3.0  # millimeters
WING_AREA_MM2 = 4.5  # square millimeters
TARGET_WING_FREQ_HZ = 200  # Drosophila: ~200 Hz

# ============================================================================
# CLASS: Insect Biomechanics Model
# ============================================================================

class InsectBiomechanics:
    """
    Kinematic model of insect flight based on measured wing trajectories.
    """

    def __init__(self, name, mass_mg, wing_span_mm, wing_area_mm2, freq_hz):
        self.name = name
        self.mass_mg = mass_mg
        self.wing_span_mm = wing_span_mm
        self.wing_area_mm2 = wing_area_mm2
        self.freq_hz = freq_hz
        self.period_s = 1.0 / freq_hz

    def wing_trajectory(self, t, phase_left=0, phase_right=np.pi):
        """
        Compute wing angle (stroke) as a function of time.

        Drosophila wing motion is approximately sinusoidal with harmonics.
        Left and right wings beat 180° out of phase (antiphase).

        Args:
            t: time array (seconds)
            phase_left: phase offset for left wing (radians)
            phase_right: phase offset for right wing (radians)

        Returns:
            stroke_left, stroke_right: stroke angle arrays (degrees)
        """
        omega = 2 * np.pi * self.freq_hz  # angular frequency (rad/s)

        # Amplitude of wing stroke: Drosophila is ~±60°
        amplitude = 60.0  # degrees

        # Fundamental sine wave + second harmonic (measured in Drosophila)
        stroke_left = amplitude * (
            0.8 * np.sin(omega * t + phase_left) +
            0.2 * np.sin(2 * omega * t + phase_left)
        )

        stroke_right = amplitude * (
            0.8 * np.sin(omega * t + phase_right) +
            0.2 * np.sin(2 * omega * t + phase_right)
        )

        return stroke_left, stroke_right

    def wing_velocity(self, t, phase_left=0, phase_right=np.pi):
        """
        Compute wing velocity (angular rate) for muscle force estimation.

        Returns:
            d_stroke_left, d_stroke_right: angular velocity (deg/s)
        """
        omega = 2 * np.pi * self.freq_hz
        amplitude_rad = np.deg2rad(60.0)

        d_stroke_left = amplitude_rad * (
            0.8 * omega * np.cos(omega * t + phase_left) +
            0.4 * omega * np.cos(2 * omega * t + phase_left)
        )

        d_stroke_right = amplitude_rad * (
            0.8 * omega * np.cos(omega * t + phase_right) +
            0.4 * omega * np.cos(2 * omega * t + phase_right)
        )

        return np.rad2deg(d_stroke_left), np.rad2deg(d_stroke_right)

    def muscle_force_required(self, t, wing_inertia_mg_mm2=0.5):
        """
        Estimate muscle force using simplified dynamic equation:
            Torque = I * dω/dt + viscous damping

        Args:
            t: time array
            wing_inertia_mg_mm2: wing moment of inertia (mg·mm²)

        Returns:
            force_left, force_right: muscle force required (mN)
        """
        stroke_left, stroke_right = self.wing_trajectory(t)

        # Angular acceleration from second derivative
        omega = 2 * np.pi * self.freq_hz
        amplitude_rad = np.deg2rad(60.0)

        d2_stroke_left = -amplitude_rad * omega**2 * (
            0.8 * np.sin(omega * t) +
            0.4 * np.sin(2 * omega * t)
        )
        d2_stroke_right = -amplitude_rad * omega**2 * (
            0.8 * np.sin(omega * t + np.pi) +
            0.4 * np.sin(2 * omega * t + np.pi)
        )

        # Torque = I * alpha + damping
        # Wing muscle lever arm is ~0.1 mm (small insects)
        lever_arm_mm = 0.1

        # Moment of inertia in conventional units (convert mg·mm² to kg·m²)
        wing_inertia_kg_m2 = wing_inertia_mg_mm2 * 1e-9  # mg·mm² → kg·m²

        torque_left = wing_inertia_kg_m2 * d2_stroke_left + 0.01 * np.rad2deg(np.deg2rad(stroke_left)) * omega
        torque_right = wing_inertia_kg_m2 * d2_stroke_right + 0.01 * np.rad2deg(np.deg2rad(stroke_right)) * omega

        # Force = Torque / lever arm (convert back to mN)
        force_left = torque_left / (lever_arm_mm * 1e-3) * 1e3  # Convert to mN
        force_right = torque_right / (lever_arm_mm * 1e-3) * 1e3

        return np.abs(force_left), np.abs(force_right)

    def control_bandwidth(self):
        """
        Estimate the control bandwidth (frequency at which insect can modulate wing force).

        Biological constraint: insects can modulate wing beat by ~20% at frequencies up to 20–50 Hz.

        Returns:
            bandwidth_hz: control bandwidth (Hz)
        """
        # Simplified: control bandwidth ≈ 0.1 × wing beat frequency
        return 0.1 * self.freq_hz

    def center_of_gravity(self):
        """
        Typical CoG location for small insects (Drosophila).
        Expressed as (x, y, z) relative to thorax centroid in mm.

        Returns:
            cog_mm: (x, y, z) position
        """
        # Drosophila CoG is typically 0.3–0.5 mm below thorax midline
        return (0.0, -0.4, 0.0)

    def moment_of_inertia(self):
        """
        Estimate body moment of inertia (needed for attitude dynamics).

        For small insects, approximate as a cylinder.
        Drosophila: ~10^-8 kg·m²

        Returns:
            Ixx, Iyy, Izz: principal moments (kg·m²)
        """
        # Rough estimate: I ≈ 0.1 * body_mass * body_length²
        body_length_mm = 3.0  # typical Drosophila
        body_length_m = body_length_mm * 1e-3
        body_mass_kg = self.mass_mg * 1e-6

        I = 0.1 * body_mass_kg * (body_length_m**2)

        return I, I, I  # Assume isotropic for simplicity


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print(f"WAVE 1: Insect Biomechanics — {INSECT}")
    print("=" * 70)
    print()

    # Initialize model
    insect = InsectBiomechanics(
        name=INSECT,
        mass_mg=BODY_MASS_MG,
        wing_span_mm=WING_SPAN_MM,
        wing_area_mm2=WING_AREA_MM2,
        freq_hz=TARGET_WING_FREQ_HZ
    )

    # Time array: 3 wing beats
    t = np.linspace(0, 3 * insect.period_s, 3000)

    # ---- WING TRAJECTORY ----
    print("1. WING KINEMATICS")
    stroke_left, stroke_right = insect.wing_trajectory(t)
    print(f"   Wing beat frequency: {insect.freq_hz} Hz")
    print(f"   Stroke amplitude: ±{np.max(np.abs(stroke_left)):.1f}°")
    print(f"   Period: {insect.period_s*1000:.2f} ms")
    print()

    # ---- MUSCLE FORCE ----
    print("2. MUSCLE DYNAMICS")
    force_left, force_right = insect.muscle_force_required(t)
    max_force = np.max(force_left)
    print(f"   Peak muscle force: {max_force:.3f} mN")
    print(f"   Duty cycle (est.): 50% (typical for insect indirect flight muscle)")
    print()

    # ---- CONTROL AUTHORITY ----
    print("3. CONTROL PROPERTIES")
    bw = insect.control_bandwidth()
    print(f"   Control bandwidth: {bw:.1f} Hz")
    cog = insect.center_of_gravity()
    print(f"   Center of gravity: ({cog[0]:.2f}, {cog[1]:.2f}, {cog[2]:.2f}) mm")
    Ixx, Iyy, Izz = insect.moment_of_inertia()
    print(f"   Body moment of inertia: {Ixx:.2e} kg·m²")
    print()

    # ---- PLOTTING ----
    print("4. GENERATING PLOTS...")
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    # Plot 1: Wing trajectory
    ax = axes[0]
    ax.plot(t*1000, stroke_left, 'b-', label='Left wing', linewidth=2)
    ax.plot(t*1000, stroke_right, 'r-', label='Right wing', linewidth=2)
    ax.set_ylabel('Stroke angle (degrees)')
    ax.set_title(f'{INSECT}: Wing Kinematics ({insect.freq_hz} Hz)')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 2: Muscle force
    ax = axes[1]
    ax.plot(t*1000, force_left, 'b-', label='Left wing', linewidth=2)
    ax.plot(t*1000, force_right, 'r-', label='Right wing', linewidth=2)
    ax.set_ylabel('Muscle force (mN)')
    ax.set_title('Estimated Wing Muscle Force')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 3: Frequency response (one period magnified)
    ax = axes[2]
    one_period = int(len(t) / 3)
    ax.plot(t[:one_period]*1000, stroke_left[:one_period], 'b-o', label='Left', markersize=4)
    ax.plot(t[:one_period]*1000, stroke_right[:one_period], 'r-s', label='Right', markersize=4)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Stroke angle (degrees)')
    ax.set_title('Single Wing Beat Cycle (antiphase)')
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig('00_insect_biomechanics/biomechanics.png', dpi=150)
    print(f"   ✓ Plot saved: 00_insect_biomechanics/biomechanics.png")
    print()

    # ---- SAVE RESULTS ----
    print("5. WRITING RESULTS to results.md...")
    with open('00_insect_biomechanics/results.md', 'w') as f:
        f.write(f"# Insect Biomechanics — Results\n\n")
        f.write(f"**Species**: {INSECT}\n\n")
        f.write(f"## Key Metrics\n\n")
        f.write(f"- **Wing beat frequency**: {insect.freq_hz} Hz\n")
        f.write(f"- **Stroke amplitude**: ±{np.max(np.abs(stroke_left)):.1f}°\n")
        f.write(f"- **Peak muscle force**: {max_force:.3f} mN\n")
        f.write(f"- **Control bandwidth**: {bw:.1f} Hz\n")
        f.write(f"- **Body mass**: {BODY_MASS_MG} mg\n")
        f.write(f"- **Wing span**: {WING_SPAN_MM} mm\n")
        f.write(f"- **Center of gravity**: ({cog[0]:.2f}, {cog[1]:.2f}, {cog[2]:.2f}) mm\n")
        f.write(f"- **Moment of inertia (Ixx)**: {Ixx:.2e} kg·m²\n\n")
        f.write(f"## Evaluation Status\n\n")
        f.write(f"Awaiting evaluator.py...\n")
    print(f"   ✓ Results saved: 00_insect_biomechanics/results.md")
    print()

    print("=" * 70)
    print("DONE. Run evaluator.py to grade results against benchmarks.")
    print("=" * 70)


if __name__ == '__main__':
    main()
