#!/usr/bin/env python3
"""
Phase 1: Test Procedures for RoboInsect v1.0
=============================================

Data logging and analysis for prototype validation:
- IMU (accelerometer + gyro) logging from nRF52 serial
- Load cell thrust measurement (Futek LSB200 10g)
- Frequency sweep analysis (50–300 Hz)
- Calibration and post-processing

Usage:
  python test_procedures.py --log_imu --log_thrust --sweep 50 300
  python test_procedures.py --calibrate_load_cell --weights 10 20 50
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
import argparse
import time
from datetime import datetime
from pathlib import Path


class RoboInsectTestSuite:
    """Test procedures and data logging for RoboInsect prototype."""

    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.data = {}
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def connect_serial(self):
        """Connect to nRF52 serial port."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"OK: Connected to {self.port} @ {self.baudrate} baud")
            time.sleep(2)  # Wait for nRF bootloader
            return True
        except Exception as e:
            print(f"ERROR: Could not connect to {self.port}: {e}")
            return False

    def disconnect_serial(self):
        """Close serial connection."""
        if self.ser:
            self.ser.close()
            print("OK: Serial connection closed")

    def log_imu(self, duration_sec=10.0, sample_rate_hz=1000):
        """
        Log IMU data (accel + gyro) from nRF52.

        Format: "IMU,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,timestamp_ms"

        Args:
            duration_sec: logging duration in seconds
            sample_rate_hz: expected sample rate (for progress display)
        """
        if not self.connect_serial():
            return False

        print(f"Logging IMU for {duration_sec} seconds ({int(duration_sec * sample_rate_hz)} samples expected)...")

        imu_data = []
        start_time = time.time()
        sample_count = 0

        while time.time() - start_time < duration_sec:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith('IMU,'):
                    parts = line.split(',')
                    if len(parts) == 8:
                        imu_data.append({
                            'accel_x': float(parts[1]),
                            'accel_y': float(parts[2]),
                            'accel_z': float(parts[3]),
                            'gyro_x': float(parts[4]),
                            'gyro_y': float(parts[5]),
                            'gyro_z': float(parts[6]),
                            'timestamp_ms': float(parts[7]),
                        })
                        sample_count += 1
                        if sample_count % 100 == 0:
                            print(f"  {sample_count} samples logged...")
            except Exception as e:
                pass

        self.disconnect_serial()
        self.data['imu'] = imu_data

        print(f"OK: Logged {len(imu_data)} IMU samples")
        print(f"  Duration: {(imu_data[-1]['timestamp_ms'] - imu_data[0]['timestamp_ms']) / 1000:.2f} sec")
        print(f"  Avg sample rate: {len(imu_data) / duration_sec:.0f} Hz")

        return imu_data

    def log_load_cell(self, duration_sec=5.0):
        """
        Log load cell (thrust) data from analog input.

        Format: "THRUST,adc_raw,voltage_mv,force_gram,timestamp_ms"

        Args:
            duration_sec: logging duration in seconds
        """
        if not self.connect_serial():
            return False

        print(f"Logging load cell for {duration_sec} seconds...")

        thrust_data = []
        start_time = time.time()

        while time.time() - start_time < duration_sec:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith('THRUST,'):
                    parts = line.split(',')
                    if len(parts) == 5:
                        thrust_data.append({
                            'adc_raw': int(parts[1]),
                            'voltage_mv': float(parts[2]),
                            'force_gram': float(parts[3]),
                            'timestamp_ms': float(parts[4]),
                        })
            except Exception as e:
                pass

        self.disconnect_serial()
        self.data['thrust'] = thrust_data

        print(f"OK: Logged {len(thrust_data)} thrust samples")
        if thrust_data:
            forces = [s['force_gram'] for s in thrust_data]
            print(f"  Force range: {min(forces):.3f} to {max(forces):.3f} g")

        return thrust_data

    def frequency_sweep(self, freq_start=50, freq_end=300, freq_step=10, dwell_sec=0.5):
        """
        Sweep actuator frequency and measure peak thrust at each frequency.

        Args:
            freq_start: start frequency (Hz)
            freq_end: end frequency (Hz)
            freq_step: frequency step (Hz)
            dwell_sec: dwell time at each frequency
        """
        if not self.connect_serial():
            return False

        frequencies = np.arange(freq_start, freq_end + freq_step, freq_step)
        sweep_data = []

        print(f"Frequency sweep: {freq_start}–{freq_end} Hz, {freq_step} Hz steps")

        for freq in frequencies:
            # Send frequency command to nRF52
            cmd = f"SWEEP,{int(freq)}\n"
            self.ser.write(cmd.encode())
            print(f"  {freq:.0f} Hz...", end='', flush=True)

            # Log thrust for dwell period
            start_time = time.time()
            thrust_samples = []

            while time.time() - start_time < dwell_sec:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith('THRUST,'):
                        parts = line.split(',')
                        if len(parts) == 5:
                            thrust_samples.append(float(parts[3]))  # force_gram
                except Exception as e:
                    pass

            if thrust_samples:
                peak_thrust = max(thrust_samples)
                sweep_data.append({'frequency': freq, 'peak_thrust_g': peak_thrust})
                print(f" {peak_thrust:.3f} g peak")
            else:
                print(f" NO DATA")

        self.disconnect_serial()
        self.data['sweep'] = sweep_data

        print(f"OK: Frequency sweep complete ({len(sweep_data)} points)")
        return sweep_data

    def calibrate_load_cell(self, weights_gram=[10, 20, 50]):
        """
        Calibrate load cell with known weights.

        Args:
            weights_gram: list of known weights in grams
        """
        if not self.connect_serial():
            return False

        print("Load cell calibration: place weights and record ADC readings")

        calibration = {}

        for weight in weights_gram:
            input(f"Place {weight}g weight on load cell and press Enter...")

            # Log for 2 seconds
            adc_readings = []
            start_time = time.time()

            while time.time() - start_time < 2.0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith('THRUST,'):
                        parts = line.split(',')
                        if len(parts) == 5:
                            adc_readings.append(int(parts[1]))  # adc_raw
                except Exception as e:
                    pass

            if adc_readings:
                avg_adc = np.mean(adc_readings)
                calibration[weight] = avg_adc
                print(f"  {weight}g: {avg_adc:.0f} ADC counts")

        self.disconnect_serial()
        self.data['calibration'] = calibration

        # Fit linear calibration curve
        if len(calibration) > 1:
            weights = np.array(list(calibration.keys()))
            adc_values = np.array(list(calibration.values()))
            coeffs = np.polyfit(adc_values, weights, 1)
            print(f"Calibration: {coeffs[0]:.6f} g/count + {coeffs[1]:.3f}")

        return calibration

    def plot_results(self):
        """Generate matplotlib plots of recorded data."""
        if 'sweep' not in self.data or not self.data['sweep']:
            print("WARNING: No frequency sweep data to plot")
            return

        fig, axes = plt.subplots(2, 2, figsize=(12, 9))

        # Plot 1: Thrust vs. Frequency
        ax = axes[0, 0]
        sweep = self.data['sweep']
        freqs = [s['frequency'] for s in sweep]
        thrusts = [s['peak_thrust_g'] for s in sweep]
        ax.plot(freqs, thrusts, 'b-o', linewidth=2, markersize=6)
        ax.set_xlabel('Frequency (Hz)', fontsize=11)
        ax.set_ylabel('Peak Thrust (g)', fontsize=11)
        ax.set_title('Actuator Thrust vs. Frequency', fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Plot 2: IMU Acceleration (if available)
        if 'imu' in self.data:
            ax = axes[0, 1]
            imu = self.data['imu']
            times = np.array([s['timestamp_ms'] for s in imu]) / 1000.0
            accel_z = np.array([s['accel_z'] for s in imu])
            ax.plot(times, accel_z, 'g-', linewidth=1)
            ax.set_xlabel('Time (s)', fontsize=11)
            ax.set_ylabel('Accel Z (m/s²)', fontsize=11)
            ax.set_title('IMU Vertical Acceleration', fontweight='bold')
            ax.grid(True, alpha=0.3)

        # Plot 3: Thrust time series
        if 'thrust' in self.data:
            ax = axes[1, 0]
            thrust = self.data['thrust']
            times = np.array([s['timestamp_ms'] for s in thrust]) / 1000.0
            forces = np.array([s['force_gram'] for s in thrust])
            ax.plot(times, forces, 'r-', linewidth=1)
            ax.set_xlabel('Time (s)', fontsize=11)
            ax.set_ylabel('Thrust (g)', fontsize=11)
            ax.set_title('Load Cell Output (Time Domain)', fontweight='bold')
            ax.grid(True, alpha=0.3)

        # Plot 4: Spectral analysis (if IMU available)
        if 'imu' in self.data:
            ax = axes[1, 1]
            imu = self.data['imu']
            accel_z = np.array([s['accel_z'] for s in imu])
            # Simple FFT
            fft_result = np.fft.fft(accel_z)
            freqs_fft = np.fft.fftfreq(len(accel_z), d=1/1000)[:len(accel_z)//2]
            power = np.abs(fft_result)[:len(accel_z)//2]
            ax.semilogy(freqs_fft, power, 'purple', linewidth=1)
            ax.set_xlabel('Frequency (Hz)', fontsize=11)
            ax.set_ylabel('Power', fontsize=11)
            ax.set_title('IMU Acceleration Spectrum', fontweight='bold')
            ax.set_xlim([0, 500])
            ax.grid(True, alpha=0.3, which='both')

        plt.tight_layout()
        output_path = f'phase1/test_results_{self.timestamp}.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"OK: Plots saved to {output_path}")
        plt.close()

    def save_csv(self):
        """Save logged data to CSV file."""
        if 'sweep' in self.data:
            csv_path = f'phase1/sweep_results_{self.timestamp}.csv'
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Frequency (Hz)', 'Peak Thrust (g)'])
                for row in self.data['sweep']:
                    writer.writerow([row['frequency'], row['peak_thrust_g']])
            print(f"OK: Sweep results saved to {csv_path}")

        if 'imu' in self.data:
            csv_path = f'phase1/imu_results_{self.timestamp}.csv'
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp (ms)', 'Accel X', 'Accel Y', 'Accel Z', 'Gyro X', 'Gyro Y', 'Gyro Z'])
                for row in self.data['imu']:
                    writer.writerow([row['timestamp_ms'], row['accel_x'], row['accel_y'], row['accel_z'],
                                     row['gyro_x'], row['gyro_y'], row['gyro_z']])
            print(f"OK: IMU data saved to {csv_path}")

        if 'thrust' in self.data:
            csv_path = f'phase1/thrust_results_{self.timestamp}.csv'
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp (ms)', 'ADC Raw', 'Voltage (mV)', 'Force (g)'])
                for row in self.data['thrust']:
                    writer.writerow([row['timestamp_ms'], row['adc_raw'], row['voltage_mv'], row['force_gram']])
            print(f"OK: Thrust data saved to {csv_path}")


def main():
    parser = argparse.ArgumentParser(description='RoboInsect Phase 1 Test Procedures')
    parser.add_argument('--port', default='/dev/ttyACM0', help='Serial port (default: /dev/ttyACM0)')
    parser.add_argument('--log_imu', action='store_true', help='Log IMU data')
    parser.add_argument('--log_thrust', action='store_true', help='Log load cell data')
    parser.add_argument('--sweep', nargs=2, type=int, metavar=('START', 'END'),
                        help='Frequency sweep (Hz). Example: --sweep 50 300')
    parser.add_argument('--calibrate_load_cell', action='store_true', help='Calibrate load cell')
    parser.add_argument('--weights', nargs='+', type=int, default=[10, 20, 50],
                        help='Weights for calibration (g). Default: 10 20 50')
    args = parser.parse_args()

    test = RoboInsectTestSuite(port=args.port)

    if args.log_imu:
        test.log_imu(duration_sec=10.0)

    if args.log_thrust:
        test.log_load_cell(duration_sec=5.0)

    if args.sweep:
        test.frequency_sweep(freq_start=args.sweep[0], freq_end=args.sweep[1], freq_step=10)

    if args.calibrate_load_cell:
        test.calibrate_load_cell(weights_gram=args.weights)

    # Generate plots and CSV
    test.plot_results()
    test.save_csv()

    print("OK: Test procedures complete")


if __name__ == '__main__':
    main()
