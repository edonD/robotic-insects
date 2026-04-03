#!/usr/bin/env python3
"""
Module 05: Structural Design & Analysis
========================================

Implements:
  - Euler-Bernoulli beam theory (wing root stiffness, deflection)
  - Modal frequency analysis (thin plate, cantilever modes)
  - Stress concentration factors at critical joints
  - Material properties (carbon fiber, aluminum)
  - Center-of-gravity and moment-of-inertia calculations

References:
  - Timoshenko & Goodier: Theory of Elasticity
  - Young & Budynas: Roark's Formulas for Stress and Strain
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import save_results_json

# ============================================================================
# MATERIAL PROPERTIES
# ============================================================================

# Carbon fiber composite (typical)
CF_DENSITY_KG_M3 = 1600
CF_YOUNGS_MODULUS_GPA = 150
CF_SHEAR_MODULUS_GPA = 7
CF_TENSILE_STRENGTH_MPA = 1200
CF_POISSON = 0.25

# Aluminum (6061-T6, used for brackets)
AL_DENSITY_KG_M3 = 2700
AL_YOUNGS_MODULUS_GPA = 69
AL_POISSON = 0.33

# ============================================================================
# CLASS: Cantilever Beam Model
# ============================================================================

class CantileverBeam:
    """
    Euler-Bernoulli cantilever beam (wing structure).

    Free-fixed boundary condition (wing root is fixed, tip is free).
    """

    def __init__(self, length_mm, width_mm, thickness_mm, youngs_modulus_gpa=150):
        self.length_m = length_mm / 1000
        self.width_m = width_mm / 1000
        self.thickness_m = thickness_mm / 1000
        self.E = youngs_modulus_gpa * 1e9  # Pa

        # Second moment of inertia (rectangular cross-section)
        # I = w * t^3 / 12
        self.I = (self.width_m * self.thickness_m**3) / 12

    def deflection_tip(self, load_n):
        """
        Tip deflection under point load at free end.

        δ = P*L^3 / (3*E*I)

        Args:
            load_n: point load at tip (Newtons)

        Returns:
            deflection_m: tip deflection in meters
        """
        deflection = (load_n * self.length_m**3) / (3 * self.E * self.I)
        return deflection

    def stiffness_n_m(self, load_n):
        """Beam stiffness (force per unit deflection)."""
        deflection = self.deflection_tip(load_n)
        if deflection > 0:
            stiffness = load_n / deflection
        else:
            stiffness = float('inf')
        return stiffness

    def first_mode_frequency_hz(self, rho_kg_m3):
        """
        First bending mode (cantilever).

        f = (λ_n^2 / (2π*L^2)) * sqrt(E*I / (ρ*A))

        where λ_1 ≈ 1.875 for cantilever
        """
        # Cross-sectional area
        A = self.width_m * self.thickness_m

        # Material density
        rho = rho_kg_m3

        # First mode eigenvalue
        lambda_1 = 1.875

        f_hz = (lambda_1**2 / (2 * np.pi * self.length_m**2)) * np.sqrt((self.E * self.I) / (rho * A))

        return f_hz

    def stress_at_root(self, load_n):
        """
        Bending stress at fixed end (root).

        σ = M*y / I, where M = P*L, y = t/2

        Args:
            load_n: point load

        Returns:
            stress_pa: bending stress in Pascals
        """
        moment = load_n * self.length_m  # M = P*L
        stress = (moment * self.thickness_m / 2) / self.I
        return stress


# ============================================================================
# CLASS: Body Structure
# ============================================================================

class RobotBody:
    """
    Robot body with simplified geometry.

    Approximated as a thin-walled cylinder with wings and tail.
    """

    def __init__(self, length_mm, diameter_mm, mass_mg):
        self.length_m = length_mm / 1000
        self.diameter_m = diameter_mm / 1000
        self.radius_m = self.diameter_m / 2
        self.mass_kg = mass_mg / 1e6

    def moment_of_inertia_roll_pitch(self):
        """
        Moment of inertia about pitch/roll axes (perpendicular to body).

        Simplified as thin-walled cylinder: I ≈ 0.25 * m * r^2
        """
        I = 0.25 * self.mass_kg * self.radius_m**2
        return I

    def moment_of_inertia_yaw(self):
        """
        Moment of inertia about yaw axis (along body).

        Simplified: I ≈ 0.5 * m * r^2
        """
        I = 0.5 * self.mass_kg * self.radius_m**2
        return I

    def natural_frequency_hz(self, youngs_modulus_gpa=150):
        """
        Approximate body natural frequency (bending modes).

        f ≈ (C / L^2) * sqrt(E / ρ)

        where C is a constant depending on boundary conditions (~50-100 for insect body)
        """
        rho = 1600  # Carbon fiber density kg/m^3
        E_pa = youngs_modulus_gpa * 1e9

        # Empirical constant for thin-walled structure
        C = 75

        f_hz = (C / (self.length_m**2)) * np.sqrt(E_pa / rho)

        return f_hz


# ============================================================================
# CLASS: Stress Concentration
# ============================================================================

class StressConcentration:
    """
    Stress concentration factors at notches and joints.

    References:
      - Heywood: Designing by Photoelasticity
      - Peterson: Stress Concentration Design Factors
    """

    @staticmethod
    def at_notch(radius_mm, depth_mm):
        """
        Stress concentration factor at a circular notch.

        K_t ≈ 1 + (2 * d/r) * (1 - sqrt(d/r))

        Args:
            radius_mm: fillet radius at notch
            depth_mm: notch depth

        Returns:
            K_t: stress concentration factor
        """
        ratio = depth_mm / radius_mm
        K_t = 1 + (2 * ratio) * (1 - np.sqrt(ratio))
        return K_t

    @staticmethod
    def at_hole(diameter_mm, plate_width_mm):
        """
        Stress concentration factor at circular hole in plate.

        K_t ≈ 3 - 3.1*(d/w) + ... (for d/w < 0.5)

        Args:
            diameter_mm: hole diameter
            plate_width_mm: plate width

        Returns:
            K_t: stress concentration factor (~3 typical)
        """
        ratio = diameter_mm / plate_width_mm
        if ratio < 0.5:
            K_t = 3 - 3.1 * ratio + 3.8 * ratio**2
        else:
            K_t = 3.0  # conservative estimate

        return K_t


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 2: Structural Design & Mechanics (Module 05)")
    print("=" * 70)
    print()

    # Wing structure (carbon fiber)
    print("1. WING STRUCTURE (Euler-Bernoulli Beam)")
    print("-" * 70)

    # Wing dimensions
    wing_length_mm = 3.0  # 3 mm span
    wing_width_mm = 0.5  # 0.5 mm chord
    wing_thickness_mm = 0.1  # 0.1 mm thickness

    wing = CantileverBeam(wing_length_mm, wing_width_mm, wing_thickness_mm,
                          youngs_modulus_gpa=CF_YOUNGS_MODULUS_GPA)

    # Thrust loads from Module 02
    wing_lift_mn = 0.003  # 3 µN per wing (extrapolated)
    wing_lift_n = wing_lift_mn / 1e6

    wing_deflection_mm = wing.deflection_tip(wing_lift_n) * 1000
    wing_stiffness = wing.stiffness_n_m(wing_lift_n)
    wing_first_mode_hz = wing.first_mode_frequency_hz(CF_DENSITY_KG_M3)
    wing_stress_pa = wing.stress_at_root(wing_lift_n)

    print(f"Length: {wing_length_mm} mm")
    print(f"Width: {wing_width_mm} mm")
    print(f"Thickness: {wing_thickness_mm} mm")
    print(f"Material: Carbon fiber composite")
    print()
    print(f"Load (thrust): {wing_lift_n*1e6:.3f} µN")
    print(f"Tip deflection: {wing_deflection_mm:.4f} mm")
    print(f"Stiffness: {wing_stiffness:.2e} N/m")
    print(f"1st bending mode: {wing_first_mode_hz:.1f} Hz")
    print(f"Stress at root: {wing_stress_pa/1e6:.2f} MPa")
    print()

    # Body structure
    print("2. BODY STRUCTURE & INERTIA")
    print("-" * 70)

    body_length_mm = 4.0
    body_diameter_mm = 1.5
    body_mass_mg = 500

    body = RobotBody(body_length_mm, body_diameter_mm, body_mass_mg)

    body_I_roll = body.moment_of_inertia_roll_pitch()
    body_I_yaw = body.moment_of_inertia_yaw()
    body_natural_freq_hz = body.natural_frequency_hz(CF_YOUNGS_MODULUS_GPA)

    print(f"Length: {body_length_mm} mm")
    print(f"Diameter: {body_diameter_mm} mm")
    print(f"Mass: {body_mass_mg} mg")
    print()
    print(f"Moment of inertia (roll/pitch): {body_I_roll:.2e} kg·m²")
    print(f"Moment of inertia (yaw): {body_I_yaw:.2e} kg·m²")
    print(f"Natural frequency (bending): {body_natural_freq_hz:.1f} Hz")
    print()

    # Stress concentration
    print("3. STRESS CONCENTRATION AT JOINTS")
    print("-" * 70)

    # Typical joint geometry: fillet notch
    fillet_radius_mm = 0.2
    notch_depth_mm = 0.05

    K_t_notch = StressConcentration.at_notch(fillet_radius_mm, notch_depth_mm)

    # Hole for pivot pin
    hole_diameter_mm = 0.3
    plate_width_mm = 1.0

    K_t_hole = StressConcentration.at_hole(hole_diameter_mm, plate_width_mm)

    print(f"Fillet notch (r={fillet_radius_mm} mm, d={notch_depth_mm} mm):")
    print(f"  Stress concentration factor K_t = {K_t_notch:.2f}")
    print()
    print(f"Pivot hole (d={hole_diameter_mm} mm, width={plate_width_mm} mm):")
    print(f"  Stress concentration factor K_t = {K_t_hole:.2f}")
    print()

    # Modal frequency sweep
    print("4. MODAL ANALYSIS (FREQUENCY SWEEP)")
    print("-" * 70)

    thicknesses_mm = np.linspace(0.05, 0.3, 20)
    frequencies_hz = []

    for t in thicknesses_mm:
        wing_variant = CantileverBeam(wing_length_mm, wing_width_mm, t,
                                      youngs_modulus_gpa=CF_YOUNGS_MODULUS_GPA)
        f = wing_variant.first_mode_frequency_hz(CF_DENSITY_KG_M3)
        frequencies_hz.append(f)

    frequencies_hz = np.array(frequencies_hz)

    print(f"1st mode frequency range: {frequencies_hz[0]:.1f} - {frequencies_hz[-1]:.1f} Hz")
    print(f"Design thickness ({wing_thickness_mm} mm): {wing_first_mode_hz:.1f} Hz")
    print()

    # Plotting
    print("5. GENERATING PLOTS...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Plot 1: Deflection vs. Load
    ax = axes[0, 0]
    loads_n = np.linspace(0, wing_lift_n * 10, 50)
    deflections_mm = [wing.deflection_tip(l) * 1000 for l in loads_n]
    ax.plot(loads_n * 1e6, deflections_mm, 'b-o', linewidth=2.5, markersize=5)
    ax.axvline(wing_lift_n * 1e6, color='r', linestyle='--', linewidth=2, label=f'Operating point')
    ax.set_xlabel('Applied Load (µN)', fontsize=11)
    ax.set_ylabel('Tip Deflection (mm)', fontsize=11)
    ax.set_title('Wing Deflection Under Load', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 2: Frequency vs. Thickness
    ax = axes[0, 1]
    ax.plot(thicknesses_mm, frequencies_hz, 'g-s', linewidth=2.5, markersize=6)
    ax.axvline(wing_thickness_mm, color='r', linestyle='--', linewidth=2, label=f'Design: {wing_first_mode_hz:.0f} Hz')
    ax.axhline(wing_first_mode_hz, color='r', linestyle='--', linewidth=2, alpha=0.5)
    ax.fill_between(thicknesses_mm, 200, 210, alpha=0.2, color='yellow', label='Control loop region')
    ax.set_xlabel('Wing Thickness (mm)', fontsize=11)
    ax.set_ylabel('1st Mode Frequency (Hz)', fontsize=11)
    ax.set_title('Modal Frequency vs. Wing Thickness', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 3: Moment of Inertia
    ax = axes[1, 0]
    categories = ['Roll/Pitch', 'Yaw']
    inertias = [body_I_roll * 1e9, body_I_yaw * 1e9]  # Convert to nanokg·m²
    colors_inertia = ['#ff7f0e', '#2ca02c']
    ax.bar(categories, inertias, color=colors_inertia, width=0.5)
    ax.set_ylabel('Moment of Inertia (nanokg·m²)', fontsize=11)
    ax.set_title('Body Inertia (Roll, Pitch, Yaw)', fontweight='bold')
    for i, v in enumerate(inertias):
        ax.text(i, v + inertias[0]*0.05, f'{v:.2f}', ha='center', fontweight='bold')

    # Plot 4: Stress at Joint vs. Load
    ax = axes[1, 1]
    loads_stress = np.linspace(0, wing_lift_n * 20, 50)
    stresses_base = np.array([wing.stress_at_root(l) / 1e6 for l in loads_stress])  # Convert to MPa
    stresses_with_concentration = stresses_base * K_t_notch

    ax.plot(loads_stress * 1e6, stresses_base, 'b-', linewidth=2.5, label='Base stress')
    ax.plot(loads_stress * 1e6, stresses_with_concentration, 'r--', linewidth=2.5, label=f'With K_t={K_t_notch:.2f}')
    ax.axhline(CF_TENSILE_STRENGTH_MPA * 0.5, color='orange', linestyle='--', linewidth=2, label='Safe limit')
    ax.axvline(wing_lift_n * 1e6, color='g', linestyle=':', linewidth=2, alpha=0.7)
    ax.set_xlabel('Applied Load (µN)', fontsize=11)
    ax.set_ylabel('Stress (MPa)', fontsize=11)
    ax.set_title('Stress Concentration at Root', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig('05_structural_design/structure_analysis.png', dpi=150, bbox_inches='tight')
    print(f"   OK: Saved: 05_structural_design/structure_analysis.png")
    print()

    # Save results markdown
    print("6. WRITING RESULTS...")
    with open('05_structural_design/results.md', 'w', encoding='utf-8') as f:
        f.write("# Structural Design & Mechanics — Results\n\n")
        f.write("**Model**: Euler-Bernoulli beam theory, modal analysis, stress concentration\n\n")
        f.write("## Wing Structure\n\n")
        f.write(f"- **Material**: Carbon fiber composite (E={CF_YOUNGS_MODULUS_GPA} GPa)\n")
        f.write(f"- **Dimensions**: {wing_length_mm} x {wing_width_mm} x {wing_thickness_mm} mm\n")
        f.write(f"- **Tip deflection**: {wing_deflection_mm:.4f} mm under {wing_lift_n*1e6:.3f} µN load\n")
        f.write(f"- **Stiffness**: {wing_stiffness:.2e} N/m\n")
        f.write(f"- **1st bending mode**: {wing_first_mode_hz:.1f} Hz\n")
        f.write(f"- **Root stress**: {wing_stress_pa/1e6:.2f} MPa\n\n")
        f.write("## Body Structure\n\n")
        f.write(f"- **Dimensions**: {body_length_mm} mm length, {body_diameter_mm} mm diameter\n")
        f.write(f"- **Mass**: {body_mass_mg} mg\n")
        f.write(f"- **I_roll/pitch**: {body_I_roll:.2e} kg·m²\n")
        f.write(f"- **I_yaw**: {body_I_yaw:.2e} kg·m²\n")
        f.write(f"- **Natural frequency**: {body_natural_freq_hz:.1f} Hz\n\n")
        f.write("## Critical Stresses\n\n")
        f.write(f"- **Wing root bending**: {wing_stress_pa/1e6:.2f} MPa\n")
        f.write(f"- **Stress concentration (fillet)**: K_t = {K_t_notch:.2f}\n")
        f.write(f"- **Stress concentration (hole)**: K_t = {K_t_hole:.2f}\n")
        f.write(f"- **Tensile strength**: {CF_TENSILE_STRENGTH_MPA} MPa\n\n")
        f.write("## Evaluation Status\n\n")
        f.write("Awaiting evaluator.py...\n")

    print(f"   OK: Saved: 05_structural_design/results.md")
    print()

    # Save JSON results
    results = {
        'wing_length_mm': float(wing_length_mm),
        'wing_width_mm': float(wing_width_mm),
        'wing_thickness_mm': float(wing_thickness_mm),
        'wing_first_mode_hz': float(wing_first_mode_hz),
        'wing_deflection_mm': float(wing_deflection_mm),
        'wing_stiffness_n_m': float(wing_stiffness),
        'wing_stress_mpa': float(wing_stress_pa / 1e6),
        'body_length_mm': float(body_length_mm),
        'body_diameter_mm': float(body_diameter_mm),
        'body_mass_mg': float(body_mass_mg),
        'body_moment_inertia_roll_kg_m2': float(body_I_roll),
        'body_moment_inertia_yaw_kg_m2': float(body_I_yaw),
        'body_natural_frequency_hz': float(body_natural_freq_hz),
        'stress_concentration_notch': float(K_t_notch),
        'stress_concentration_hole': float(K_t_hole),
    }
    save_results_json('05_structural_design', results)

    print("=" * 70)
    print("DONE. Structural analysis complete. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
