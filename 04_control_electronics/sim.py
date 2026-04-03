#!/usr/bin/env python3
"""
Module 04: Control Electronics & Real-Time Systems
===================================================

Models:
  - BLE wireless latency and connection overhead
  - MCU duty cycle (active vs. sleep modes)
  - ADC resolution and noise floor (6-bit ENOB typical)
  - Control loop jitter (timing variability ±5%)
  - Sensor-to-actuator latency budget

Reference: Real-time embedded systems design for microrobots
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import save_results_json

# ============================================================================
# CONTROL PARAMETERS
# ============================================================================

# Control loop timing
CONTROL_LOOP_FREQ_HZ = 100  # 100 Hz main control loop
CONTROL_SAMPLE_TIME_MS = 1000 / CONTROL_LOOP_FREQ_HZ  # 10 ms per cycle

# Wireless communication (BLE 5.0)
BLE_ADVERTISING_INTERVAL_MS = 20  # BLE advertisement interval
BLE_CONNECTION_LATENCY_MS = 2.0  # BLE latency (2 ms typical)
BLE_FRAME_SIZE_BYTES = 20  # BLE ATT payload
BLE_DATA_RATE_KBPS = 1000  # 1 Mbps (BLE 5.0)

# MCU specifications (STM32L or similar)
MCU_CLOCK_MHZ = 16  # 16 MHz clock
MCU_ACTIVE_CURRENT_MA = 8  # mA during operation
MCU_SLEEP_CURRENT_UA = 50  # µA in sleep mode

# ADC (12-bit, but limited by noise)
ADC_RESOLUTION_BITS = 12
ADC_ENOB_BITS = 6.5  # Effective Number of Bits (typical ~6.5 for real ADC)
ADC_SAMPLING_RATE_HZ = 1000  # 1 kHz sample rate
ADC_INPUT_RANGE_MV = 3300  # 3.3V rail

# Sensor specifications (IMU: ICM-20689)
IMU_GYRO_NOISE_DPS = 0.5  # degrees/sec RMS noise
IMU_ACCEL_NOISE_MG = 10  # milliG RMS noise
IMU_UPDATE_RATE_HZ = 1000  # 1 kHz output rate

# ============================================================================
# CLASS: Wireless Transceiver Model
# ============================================================================

class BLETransceiver:
    """
    BLE wireless transceiver latency and overhead model.
    """

    def __init__(self, advertising_interval_ms=20, connection_latency_ms=2.0):
        self.adv_interval_ms = advertising_interval_ms
        self.conn_latency_ms = connection_latency_ms

    def message_latency_ms(self, message_bytes):
        """
        Compute one-way message latency including BLE overhead.

        Args:
            message_bytes: payload size in bytes

        Returns:
            latency_ms: end-to-end latency in milliseconds
        """
        # BLE frame overhead: ~11 bytes (preamble, access address, CRC, etc.)
        total_bytes = message_bytes + 11

        # Transmission time at 1 Mbps = 8 µs per byte
        tx_time_ms = total_bytes * 8 / 1000

        # Add connection latency (2 ms typical for BLE)
        total_latency = tx_time_ms + self.conn_latency_ms

        return total_latency

    def roundtrip_latency_ms(self, request_bytes, response_bytes):
        """Compute request-response roundtrip latency."""
        request_latency = self.message_latency_ms(request_bytes)
        response_latency = self.message_latency_ms(response_bytes)
        return request_latency + response_latency


# ============================================================================
# CLASS: MCU Control Loop
# ============================================================================

class MCUController:
    """
    Real-time control loop with duty cycle and jitter analysis.
    """

    def __init__(self, loop_freq_hz, active_current_ma, sleep_current_ua):
        self.loop_freq_hz = loop_freq_hz
        self.loop_period_ms = 1000 / loop_freq_hz
        self.active_current_ma = active_current_ma
        self.sleep_current_ua = sleep_current_ua

    def duty_cycle_analysis(self, computation_ms_per_loop):
        """
        Compute MCU duty cycle (fraction of time in active mode).

        Args:
            computation_ms_per_loop: time spent in active computation per loop

        Returns:
            duty_cycle: fraction [0, 1]
            sleep_time_ms: time available for sleep
        """
        duty_cycle = computation_ms_per_loop / self.loop_period_ms
        duty_cycle = np.clip(duty_cycle, 0, 1)
        sleep_time_ms = self.loop_period_ms * (1 - duty_cycle)

        return duty_cycle, sleep_time_ms

    def average_current_ma(self, duty_cycle):
        """
        Estimate average MCU current over time.

        I_avg = I_active * duty_cycle + I_sleep * (1 - duty_cycle)
        """
        sleep_current_ma = self.sleep_current_ua / 1000
        avg_current = (self.active_current_ma * duty_cycle +
                       sleep_current_ma * (1 - duty_cycle))
        return avg_current

    def timing_jitter_analysis(self, jitter_percent=5.0):
        """
        Analyze control loop timing jitter.

        Typical: ±5% jitter due to interrupt handling, OS overhead.
        """
        jitter_ratio = jitter_percent / 100
        nominal_period_ms = self.loop_period_ms
        jitter_ms = nominal_period_ms * jitter_ratio
        max_period_ms = nominal_period_ms + jitter_ms
        min_period_ms = nominal_period_ms - jitter_ms

        return jitter_ms, min_period_ms, max_period_ms


# ============================================================================
# CLASS: ADC Model
# ============================================================================

class ADCConverter:
    """
    Analog-to-digital converter with noise floor analysis.
    """

    def __init__(self, resolution_bits, enob_bits, input_range_mv):
        self.resolution_bits = resolution_bits
        self.enob_bits = enob_bits
        self.input_range_mv = input_range_mv

    def lsb_voltage_mv(self):
        """Least significant bit in millivolts."""
        return self.input_range_mv / (2 ** self.resolution_bits)

    def noise_floor_mv(self):
        """
        Effective noise floor based on ENOB.

        Noise = LSB / sqrt(12) * sqrt(2^(resolution - ENOB))
        """
        lsb = self.lsb_voltage_mv()
        noise_factor = np.sqrt(2 ** (self.resolution_bits - self.enob_bits))
        noise = lsb / np.sqrt(12) * noise_factor
        return noise

    def snr_db(self):
        """
        Signal-to-noise ratio with full-scale input.

        SNR = 6.02 * ENOB + 1.76 dB
        """
        snr = 6.02 * self.enob_bits + 1.76
        return snr


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 2: Control Electronics & Real-Time Systems (Module 04)")
    print("=" * 70)
    print()

    # BLE transceiver
    print("1. WIRELESS COMMUNICATION (BLE)")
    print("-" * 70)
    ble = BLETransceiver(BLE_ADVERTISING_INTERVAL_MS, BLE_CONNECTION_LATENCY_MS)

    # Typical sensor telemetry: ~8 bytes (3x gyro + 1x status)
    sensor_message_bytes = 8
    command_message_bytes = 4

    sensor_latency = ble.message_latency_ms(sensor_message_bytes)
    command_latency = ble.message_latency_ms(command_message_bytes)
    roundtrip_latency = ble.roundtrip_latency_ms(sensor_message_bytes, command_message_bytes)

    print(f"BLE standard: 5.0 (1 Mbps)")
    print(f"Sensor telemetry latency ({sensor_message_bytes} bytes): {sensor_latency:.2f} ms")
    print(f"Command latency ({command_message_bytes} bytes): {command_latency:.2f} ms")
    print(f"Round-trip latency: {roundtrip_latency:.2f} ms")
    print()

    # MCU control loop
    print("2. MCU CONTROL LOOP & TIMING")
    print("-" * 70)
    mcu = MCUController(CONTROL_LOOP_FREQ_HZ, MCU_ACTIVE_CURRENT_MA, MCU_SLEEP_CURRENT_UA)

    # Assume 3 ms of computation per loop (PID, sensor fusion, etc.)
    computation_ms = 3.0
    duty_cycle, sleep_time_ms = mcu.duty_cycle_analysis(computation_ms)
    avg_current = mcu.average_current_ma(duty_cycle)

    print(f"Loop frequency: {CONTROL_LOOP_FREQ_HZ} Hz")
    print(f"Loop period: {mcu.loop_period_ms:.1f} ms")
    print(f"Computation time: {computation_ms:.1f} ms per loop")
    print(f"Duty cycle: {duty_cycle*100:.1f}%")
    print(f"Sleep time available: {sleep_time_ms:.1f} ms")
    print(f"Average MCU current: {avg_current:.2f} mA")
    print()

    # Timing jitter
    print("3. CONTROL LOOP JITTER ANALYSIS")
    print("-" * 70)
    jitter_ms, min_period_ms, max_period_ms = mcu.timing_jitter_analysis(jitter_percent=5.0)

    print(f"Nominal period: {mcu.loop_period_ms:.2f} ms")
    print(f"Jitter (±5%): ±{jitter_ms:.2f} ms")
    print(f"Min period: {min_period_ms:.2f} ms ({max_period_ms/min_period_ms:.3f}x slower)")
    print(f"Max period: {max_period_ms:.2f} ms ({max_period_ms/min_period_ms:.3f}x faster)")
    print()

    # ADC analysis
    print("4. ADC NOISE & RESOLUTION")
    print("-" * 70)
    adc = ADCConverter(ADC_RESOLUTION_BITS, ADC_ENOB_BITS, ADC_INPUT_RANGE_MV)

    lsb_mv = adc.lsb_voltage_mv()
    noise_floor_mv = adc.noise_floor_mv()
    snr = adc.snr_db()

    print(f"Resolution: {ADC_RESOLUTION_BITS} bits")
    print(f"ENOB (Effective): {ADC_ENOB_BITS:.1f} bits")
    print(f"LSB voltage: {lsb_mv:.2f} mV")
    print(f"Noise floor: {noise_floor_mv:.2f} mV RMS")
    print(f"SNR (full-scale): {snr:.1f} dB")
    print(f"Sampling rate: {ADC_SAMPLING_RATE_HZ} Hz")
    print()

    # Latency budget
    print("5. LATENCY BUDGET (sensor to actuator)")
    print("-" * 70)
    imu_latency = 1000 / IMU_UPDATE_RATE_HZ  # 1 ms typical
    control_latency = mcu.loop_period_ms  # 10 ms (next control update)
    actuation_latency = 2.0  # ~2 ms for piezo response
    total_latency = imu_latency + control_latency + actuation_latency + roundtrip_latency

    print(f"IMU measurement latency: {imu_latency:.1f} ms (1 kHz update)")
    print(f"Control loop latency: {control_latency:.1f} ms")
    print(f"Wireless (BLE) latency: {roundtrip_latency:.2f} ms")
    print(f"Actuation latency: {actuation_latency:.1f} ms")
    print(f"Total sensor-to-actuator latency: {total_latency:.2f} ms")
    print(f"Latency as fraction of control period: {total_latency/control_latency:.2f}x")
    print()

    # Plotting
    print("6. GENERATING PLOTS...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Plot 1: Duty cycle vs. computation time
    ax = axes[0, 0]
    comp_times = np.linspace(0, mcu.loop_period_ms, 50)
    duty_cycles = [mcu.duty_cycle_analysis(ct)[0] for ct in comp_times]
    ax.plot(comp_times, np.array(duty_cycles)*100, 'b-o', linewidth=2.5, markersize=5)
    ax.axvline(computation_ms, color='r', linestyle='--', linewidth=2, label=f'Current: {computation_ms} ms')
    ax.axhline(duty_cycle*100, color='r', linestyle='--', linewidth=2, alpha=0.5)
    ax.set_xlabel('Computation Time per Loop (ms)', fontsize=11)
    ax.set_ylabel('Duty Cycle (%)', fontsize=11)
    ax.set_title('MCU Duty Cycle Analysis', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_ylim([0, 100])

    # Plot 2: Average current vs. duty cycle
    ax = axes[0, 1]
    duty_range = np.linspace(0, 1, 50)
    avg_currents = [mcu.average_current_ma(dc) for dc in duty_range]
    ax.plot(duty_range*100, avg_currents, 'g-s', linewidth=2.5, markersize=5)
    ax.axvline(duty_cycle*100, color='r', linestyle='--', linewidth=2, label=f'Current: {duty_cycle*100:.1f}%')
    ax.axhline(avg_current, color='r', linestyle='--', linewidth=2, alpha=0.5)
    ax.set_xlabel('Duty Cycle (%)', fontsize=11)
    ax.set_ylabel('Average Current (mA)', fontsize=11)
    ax.set_title('MCU Power Consumption', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 3: Control loop timing distribution (jitter)
    ax = axes[1, 0]
    periods = np.random.normal(mcu.loop_period_ms, jitter_ms, 1000)
    periods = np.clip(periods, min_period_ms, max_period_ms)
    ax.hist(periods, bins=30, color='purple', alpha=0.7, edgecolor='black')
    ax.axvline(mcu.loop_period_ms, color='r', linestyle='--', linewidth=2, label='Nominal')
    ax.axvline(min_period_ms, color='orange', linestyle='--', linewidth=2, label='Min/Max')
    ax.axvline(max_period_ms, color='orange', linestyle='--', linewidth=2)
    ax.set_xlabel('Loop Period (ms)', fontsize=11)
    ax.set_ylabel('Occurrences', fontsize=11)
    ax.set_title(f'Control Loop Jitter Distribution (±5%)', fontweight='bold')
    ax.legend()

    # Plot 4: ADC Noise Floor vs. Input Signal
    ax = axes[1, 1]
    signal_amplitudes_mv = np.logspace(0, np.log10(ADC_INPUT_RANGE_MV), 50)
    snr_values = []
    for amp in signal_amplitudes_mv:
        signal_power = (amp / np.sqrt(2)) ** 2
        noise_power = noise_floor_mv ** 2
        snr_linear = signal_power / noise_power
        snr_db_val = 10 * np.log10(snr_linear)
        snr_values.append(snr_db_val)

    ax.semilogx(signal_amplitudes_mv, snr_values, 'orange', linewidth=2.5, marker='s', markersize=6)
    ax.axhline(snr, color='r', linestyle='--', linewidth=2, label=f'Full-scale SNR: {snr:.1f} dB')
    ax.axhline(0, color='k', linestyle='-', linewidth=1, alpha=0.3)
    ax.set_xlabel('Input Signal Amplitude (mV)', fontsize=11)
    ax.set_ylabel('SNR (dB)', fontsize=11)
    ax.set_title('ADC Signal-to-Noise Ratio', fontweight='bold')
    ax.grid(True, alpha=0.3, which='both')
    ax.legend()

    plt.tight_layout()
    plt.savefig('04_control_electronics/control_analysis.png', dpi=150, bbox_inches='tight')
    print(f"   OK: Saved: 04_control_electronics/control_analysis.png")
    print()

    # Save results markdown
    print("7. WRITING RESULTS...")
    with open('04_control_electronics/results.md', 'w', encoding='utf-8') as f:
        f.write("# Control Electronics & Real-Time Systems — Results\n\n")
        f.write("**Model**: BLE communication, MCU duty cycle, ADC noise, timing jitter\n\n")
        f.write("## Wireless Communication (BLE 5.0)\n\n")
        f.write(f"- **Sensor latency**: {sensor_latency:.2f} ms ({sensor_message_bytes} bytes)\n")
        f.write(f"- **Command latency**: {command_latency:.2f} ms ({command_message_bytes} bytes)\n")
        f.write(f"- **Round-trip latency**: {roundtrip_latency:.2f} ms\n\n")
        f.write("## MCU Control Loop\n\n")
        f.write(f"- **Frequency**: {CONTROL_LOOP_FREQ_HZ} Hz\n")
        f.write(f"- **Period**: {mcu.loop_period_ms:.1f} ms\n")
        f.write(f"- **Computation time**: {computation_ms:.1f} ms\n")
        f.write(f"- **Duty cycle**: {duty_cycle*100:.1f}%\n")
        f.write(f"- **Average current**: {avg_current:.2f} mA\n\n")
        f.write("## Timing Jitter\n\n")
        f.write(f"- **Jitter**: ±{jitter_ms:.2f} ms (±5%)\n")
        f.write(f"- **Min period**: {min_period_ms:.2f} ms\n")
        f.write(f"- **Max period**: {max_period_ms:.2f} ms\n\n")
        f.write("## ADC Specifications\n\n")
        f.write(f"- **Resolution**: {ADC_RESOLUTION_BITS} bits\n")
        f.write(f"- **ENOB**: {ADC_ENOB_BITS:.1f} bits\n")
        f.write(f"- **LSB**: {lsb_mv:.2f} mV\n")
        f.write(f"- **Noise floor**: {noise_floor_mv:.2f} mV RMS\n")
        f.write(f"- **SNR (full-scale)**: {snr:.1f} dB\n\n")
        f.write("## End-to-End Latency\n\n")
        f.write(f"- **Total sensor-to-actuator**: {total_latency:.2f} ms\n")
        f.write(f"- **As fraction of control period**: {total_latency/control_latency:.2f}x\n\n")
        f.write("## Evaluation Status\n\n")
        f.write("Awaiting evaluator.py...\n")

    print(f"   OK: Saved: 04_control_electronics/results.md")
    print()

    # Save JSON results
    results = {
        'control_frequency_hz': float(CONTROL_LOOP_FREQ_HZ),
        'control_period_ms': float(mcu.loop_period_ms),
        'ble_sensor_latency_ms': float(sensor_latency),
        'ble_command_latency_ms': float(command_latency),
        'ble_roundtrip_latency_ms': float(roundtrip_latency),
        'mcu_duty_cycle_percent': float(duty_cycle * 100),
        'mcu_average_current_ma': float(avg_current),
        'control_jitter_ms': float(jitter_ms),
        'control_jitter_percent': 5.0,
        'adc_resolution_bits': int(ADC_RESOLUTION_BITS),
        'adc_enob_bits': float(ADC_ENOB_BITS),
        'adc_lsb_mv': float(lsb_mv),
        'adc_noise_floor_mv': float(noise_floor_mv),
        'adc_snr_db': float(snr),
        'total_latency_ms': float(total_latency),
        'latency_to_period_ratio': float(total_latency / control_latency),
    }
    save_results_json('04_control_electronics', results)

    print("=" * 70)
    print("DONE. Control electronics analysis complete. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
