#!/usr/bin/env python3
"""
Module 03: Power Management & Battery Analysis
==============================================

Implements:
  - Peukert's Law for non-ideal battery discharge
  - Actuator efficiency model (mechanical output / electrical input)
  - Thermal dissipation (Joule heating in electronics)
  - Flight time vs. mass tradeoff analysis
  - Battery discharge curves under variable loads

References:
  - Peukert, W. (1897). "On the Dependence of Capacity on Discharge Current"
  - Typical Li-poly battery discharge characteristics
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import save_results_json

# ============================================================================
# BATTERY & POWER PARAMETERS
# ============================================================================

# From Module 01 & 02 (actuator and aerodynamics)
ACTUATOR_POWER_MW = 20.0  # mW (from Module 01 at 200 Hz)
CONTROLLER_POWER_MW = 5.0  # mW (microcontroller + comm)
SENSOR_POWER_MW = 2.0  # mW (IMU + pressure sensor)
COMMUNICATION_POWER_MW = 8.0  # mW (BLE transceiver)
MARGIN_POWER_MW = 5.0  # Power margin (5%)

TOTAL_IDLE_POWER_MW = CONTROLLER_POWER_MW + SENSOR_POWER_MW

# Battery specifications
BATTERY_NOMINAL_VOLTAGE_V = 3.7  # Li-poly nominal
BATTERY_CAPACITY_MAH = 50  # 50 mAh battery
BATTERY_CAPACITY_WHR = (BATTERY_NOMINAL_VOLTAGE_V * BATTERY_CAPACITY_MAH) / 1000

# Peukert exponent (typical for Li-poly: 1.05-1.15)
PEUKERT_K = 1.1  # dimensionless

# Temperature effects
NOMINAL_TEMP_C = 25
TEMP_COEFFICIENT = 0.004  # capacity loss per 1°C above nominal

# ============================================================================
# CLASS: Battery Model with Peukert's Law
# ============================================================================

class LiPolyBattery:
    """
    Li-poly battery with Peukert's law discharge model.

    Peukert's law: t = H / (I^k)
    where:
        t = discharge time (hours)
        H = battery capacity rating (Ah)
        I = discharge current (A)
        k = Peukert exponent (1.0 = ideal, >1.0 = real battery)
    """

    def __init__(self, capacity_mah, nominal_voltage_v, peukert_k=1.1):
        self.capacity_mah = capacity_mah
        self.capacity_ah = capacity_mah / 1000
        self.nominal_voltage_v = nominal_voltage_v
        self.peukert_k = peukert_k
        self.energy_whr = (nominal_voltage_v * capacity_mah) / 1000

    def discharge_time_hours(self, current_ma):
        """
        Compute discharge time using Peukert's law.

        Args:
            current_ma: discharge current (milliamps)

        Returns:
            time_hours: time until fully discharged
        """
        current_a = current_ma / 1000
        time_hours = self.capacity_ah / (current_a ** (self.peukert_k - 1))
        return time_hours

    def discharge_time_minutes(self, current_ma):
        """Return discharge time in minutes."""
        return self.discharge_time_hours(current_ma) * 60

    def available_energy_wh(self, discharge_current_ma, temp_c=25):
        """
        Compute available energy accounting for temperature.

        Args:
            discharge_current_ma: current draw (mA)
            temp_c: battery temperature (Celsius)

        Returns:
            energy_wh: available energy in Wh
        """
        # Temperature derating
        temp_margin = max(0, (temp_c - NOMINAL_TEMP_C) * TEMP_COEFFICIENT)
        derating = 1.0 - temp_margin

        # Effective discharge time
        t_hours = self.discharge_time_hours(discharge_current_ma)

        # Energy = V * I * t, accounting for Peukert losses
        current_a = discharge_current_ma / 1000
        energy_wh = self.nominal_voltage_v * current_a * t_hours * derating

        return energy_wh


# ============================================================================
# EFFICIENCY & THERMAL MODEL
# ============================================================================

class PowerBudget:
    """
    Complete power budget with actuator efficiency and thermal dissipation.
    """

    def __init__(self, actuator_mw, controller_mw, sensor_mw, comm_mw, margin_mw):
        self.actuator_mw = actuator_mw
        self.controller_mw = controller_mw
        self.sensor_mw = sensor_mw
        self.comm_mw = comm_mw
        self.margin_mw = margin_mw
        self.total_mw = actuator_mw + controller_mw + sensor_mw + comm_mw + margin_mw

    def actuator_efficiency(self, electrical_power_mw):
        """
        Estimate mechanical output power from piezoelectric actuators.

        PZT actuators are typically 60-80% efficient.
        """
        efficiency = 0.70
        mechanical_power_mw = electrical_power_mw * efficiency
        return mechanical_power_mw

    def thermal_dissipation(self, electrical_power_mw):
        """
        Power dissipated as heat (Joule heating).

        Q = I²R or Q = (1 - η) × P_in
        """
        efficiency = 0.70
        heat_mw = electrical_power_mw * (1 - efficiency)
        return heat_mw

    def total_power_budget(self, include_margin=True):
        """Total power consumption (mW)."""
        total = self.actuator_mw + self.controller_mw + self.sensor_mw + self.comm_mw
        if include_margin:
            total += self.margin_mw
        return total


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 2: Power Management & Battery (Module 03)")
    print("=" * 70)
    print()

    # Battery model
    print("1. BATTERY SPECIFICATIONS")
    print("-" * 70)
    battery = LiPolyBattery(BATTERY_CAPACITY_MAH, BATTERY_NOMINAL_VOLTAGE_V, PEUKERT_K)
    print(f"Chemistry: Li-poly (3.7V nominal)")
    print(f"Capacity: {BATTERY_CAPACITY_MAH} mAh")
    print(f"Energy: {battery.energy_whr:.2f} Wh")
    print(f"Peukert exponent: {PEUKERT_K}")
    print()

    # Power budget
    print("2. POWER BUDGET")
    print("-" * 70)
    power_budget = PowerBudget(
        ACTUATOR_POWER_MW,
        CONTROLLER_POWER_MW,
        SENSOR_POWER_MW,
        COMMUNICATION_POWER_MW,
        MARGIN_POWER_MW
    )

    total_power = power_budget.total_power_budget()
    idle_power = TOTAL_IDLE_POWER_MW

    print(f"Actuator power: {ACTUATOR_POWER_MW} mW")
    print(f"Controller power: {CONTROLLER_POWER_MW} mW")
    print(f"Sensor power: {SENSOR_POWER_MW} mW")
    print(f"Communication power: {COMMUNICATION_POWER_MW} mW")
    print(f"Margin (5%): {MARGIN_POWER_MW} mW")
    print(f"Total power: {total_power} mW")
    print()

    # Flight time analysis
    print("3. FLIGHT TIME ANALYSIS (Peukert's Law)")
    print("-" * 70)

    # Convert total power to equivalent discharge current
    # P = V * I → I = P / V
    discharge_current_ma = (total_power / 1000) / BATTERY_NOMINAL_VOLTAGE_V * 1000

    flight_time_min_ideal = battery.discharge_time_minutes(discharge_current_ma)
    flight_time_min_actual = battery.discharge_time_minutes(discharge_current_ma)  # Already includes Peukert

    print(f"Average current draw: {discharge_current_ma:.2f} mA")
    print(f"Discharge time (Peukert): {flight_time_min_actual:.2f} minutes")
    print(f"Discharge time (hours): {flight_time_min_actual/60:.3f} h")
    print()

    # Efficiency analysis
    print("4. ACTUATOR EFFICIENCY & THERMAL")
    print("-" * 70)
    actuator_mech_mw = power_budget.actuator_efficiency(ACTUATOR_POWER_MW)
    actuator_heat_mw = power_budget.thermal_dissipation(ACTUATOR_POWER_MW)

    print(f"Electrical input: {ACTUATOR_POWER_MW} mW")
    print(f"Mechanical output: {actuator_mech_mw:.2f} mW")
    print(f"Thermal loss: {actuator_heat_mw:.2f} mW")
    print(f"Efficiency: 70% (typical for PZT)")
    print()

    # Flight time vs. payload mass tradeoff
    print("5. FLIGHT TIME vs. PAYLOAD MASS TRADEOFF")
    print("-" * 70)

    # Assume baseline mass = 0.5g, battery adds 0.2g
    # Additional payload increases hover thrust requirement
    baseline_mass_mg = 500
    battery_mass_mg = 200

    # Hover thrust = weight
    # Need to increase thrust at higher mass → higher power consumption (quadratic relationship)
    payload_masses_mg = np.array([0, 100, 200, 300, 400, 500])
    flight_times_min = []

    for payload_mg in payload_masses_mg:
        total_mass_mg = baseline_mass_mg + battery_mass_mg + payload_mg
        # Power scales with weight (approximately cubic with mass for wing frequency)
        # F_thrust ∝ m, P ∝ F * v ∝ m * sqrt(m) ∝ m^1.5
        mass_ratio = total_mass_mg / baseline_mass_mg
        power_scaling = mass_ratio ** 1.5  # empirical scaling
        adjusted_power_mw = total_power * power_scaling

        adjusted_current_ma = (adjusted_power_mw / 1000) / BATTERY_NOMINAL_VOLTAGE_V * 1000
        flight_time_min = battery.discharge_time_minutes(adjusted_current_ma)
        flight_times_min.append(flight_time_min)

    flight_times_min = np.array(flight_times_min)

    print("Payload mass vs. flight time:")
    for payload_mg, flight_time in zip(payload_masses_mg, flight_times_min):
        print(f"  {payload_mg:3.0f} mg payload -> {flight_time:6.2f} min flight time")
    print()

    # Plotting
    print("6. GENERATING PLOTS...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Plot 1: Discharge curves (Peukert effect)
    ax = axes[0, 0]
    currents = np.linspace(50, 500, 30)
    discharge_times = [battery.discharge_time_minutes(i) for i in currents]
    ax.plot(currents, discharge_times, 'b-o', linewidth=2.5, markersize=5)
    ax.axvline(discharge_current_ma, color='r', linestyle='--', linewidth=2, label=f'Operating point ({discharge_current_ma:.0f} mA)')
    ax.set_xlabel('Discharge Current (mA)', fontsize=11)
    ax.set_ylabel('Flight Time (minutes)', fontsize=11)
    ax.set_title('Battery Discharge Time (Peukert\'s Law)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 2: Power budget breakdown
    ax = axes[0, 1]
    power_categories = ['Actuator', 'Controller', 'Sensor', 'Comm', 'Margin']
    power_values = [ACTUATOR_POWER_MW, CONTROLLER_POWER_MW, SENSOR_POWER_MW,
                    COMMUNICATION_POWER_MW, MARGIN_POWER_MW]
    colors = ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728', '#9467bd']
    ax.pie(power_values, labels=power_categories, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title(f'Power Budget ({total_power} mW total)', fontweight='bold')

    # Plot 3: Efficiency breakdown
    ax = axes[1, 0]
    categories = ['Mechanical\noutput', 'Thermal\nloss']
    values = [actuator_mech_mw, actuator_heat_mw]
    colors_eff = ['#2ca02c', '#d62728']
    ax.bar(categories, values, color=colors_eff, width=0.5)
    ax.set_ylabel('Power (mW)', fontsize=11)
    ax.set_title('Actuator Efficiency (70%)', fontweight='bold')
    ax.set_ylim([0, ACTUATOR_POWER_MW * 1.2])
    for i, v in enumerate(values):
        ax.text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')

    # Plot 4: Flight time vs. payload
    ax = axes[1, 1]
    ax.plot(payload_masses_mg, flight_times_min, 'g-s', linewidth=2.5, markersize=8)
    ax.fill_between(payload_masses_mg, flight_times_min, alpha=0.2, color='green')
    ax.set_xlabel('Payload Mass (mg)', fontsize=11)
    ax.set_ylabel('Flight Time (minutes)', fontsize=11)
    ax.set_title('Flight Time vs. Payload Trade-off', fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('03_power_management/power_analysis.png', dpi=150, bbox_inches='tight')
    print(f"   OK: Saved: 03_power_management/power_analysis.png")
    print()

    # Save results markdown
    print("7. WRITING RESULTS...")
    with open('03_power_management/results.md', 'w', encoding='utf-8') as f:
        f.write("# Power Management & Battery — Results\n\n")
        f.write("**Model**: Peukert's Law battery discharge with efficiency analysis\n\n")
        f.write("## Battery Specifications\n\n")
        f.write(f"- **Chemistry**: Li-poly (3.7V nominal)\n")
        f.write(f"- **Capacity**: {BATTERY_CAPACITY_MAH} mAh\n")
        f.write(f"- **Energy**: {battery.energy_whr:.2f} Wh\n")
        f.write(f"- **Peukert exponent**: {PEUKERT_K}\n\n")
        f.write("## Power Budget\n\n")
        f.write(f"- **Total power**: {total_power} mW\n")
        f.write(f"  - Actuators: {ACTUATOR_POWER_MW} mW\n")
        f.write(f"  - Controller: {CONTROLLER_POWER_MW} mW\n")
        f.write(f"  - Sensors: {SENSOR_POWER_MW} mW\n")
        f.write(f"  - Communication: {COMMUNICATION_POWER_MW} mW\n\n")
        f.write("## Flight Time\n\n")
        f.write(f"- **Discharge current**: {discharge_current_ma:.2f} mA\n")
        f.write(f"- **Flight time**: {flight_time_min_actual:.2f} minutes\n")
        f.write(f"- **Flight duration**: {flight_time_min_actual/60:.3f} hours\n\n")
        f.write("## Efficiency Analysis\n\n")
        f.write(f"- **Actuator electrical input**: {ACTUATOR_POWER_MW} mW\n")
        f.write(f"- **Mechanical output**: {actuator_mech_mw:.2f} mW (70%)\n")
        f.write(f"- **Thermal loss**: {actuator_heat_mw:.2f} mW\n\n")
        f.write("## Evaluation Status\n\n")
        f.write("Awaiting evaluator.py...\n")

    print(f"   OK: Saved: 03_power_management/results.md")
    print()

    # Save JSON results
    results = {
        'battery_capacity_mah': float(BATTERY_CAPACITY_MAH),
        'battery_voltage_v': float(BATTERY_NOMINAL_VOLTAGE_V),
        'battery_energy_whr': float(battery.energy_whr),
        'peukert_exponent': float(PEUKERT_K),
        'total_power_mw': float(total_power),
        'actuator_power_mw': float(ACTUATOR_POWER_MW),
        'controller_power_mw': float(CONTROLLER_POWER_MW),
        'sensor_power_mw': float(SENSOR_POWER_MW),
        'communication_power_mw': float(COMMUNICATION_POWER_MW),
        'discharge_current_ma': float(discharge_current_ma),
        'flight_time_minutes': float(flight_time_min_actual),
        'flight_time_hours': float(flight_time_min_actual / 60),
        'actuator_efficiency_percent': 70.0,
        'actuator_mechanical_power_mw': float(actuator_mech_mw),
        'actuator_thermal_loss_mw': float(actuator_heat_mw),
    }
    save_results_json('03_power_management', results)

    print("=" * 70)
    print("DONE. Power analysis complete. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
