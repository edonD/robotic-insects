# Phase 1: Calibration Guide — RoboInsect v1.0

**Objective**: Establish baseline performance and validate design assumptions  
**Timeline**: ~2 hours post-assembly  
**Pass Criteria**: Thrust > 1 mN, resonance frequency within 150–250 Hz, CoG ±2 mm accuracy  

---

## 1. Wing Resonance Calibration

**Procedure**:
1. Apply sine wave sweep (10–300 Hz) to one actuator at 20% PWM amplitude
2. Record wing acceleration using IMU
3. Identify peak acceleration frequency — this is the natural frequency
4. Expected: 180–220 Hz (tuned for 200 Hz wing beat)
5. If wrong:
   - Too high (>250 Hz): add small weight to wing tip
   - Too low (<150 Hz): may indicate delamination (re-epoxy wing-actuator bond)

**Data Recording**:
```bash
python phase1/test_procedures.py --sweep 10 300 --log_imu
```

**Pass Criteria**: Resonance peak within ±20 Hz of 200 Hz design target

---

## 2. Thrust Calibration

**Procedure**:
1. Mount prototype on load cell (Futek LSB200 or equivalent)
2. Calibrate load cell with known weights (10g, 20g, 50g) using:
   ```bash
   python phase1/test_procedures.py --calibrate_load_cell --weights 10 20 50
   ```
3. Run frequency sweep at fixed 20V drive voltage:
   ```bash
   python phase1/test_procedures.py --sweep 50 300 --log_thrust
   ```
4. Extract peak thrust from results CSV
5. Expected: 1–5 mN depending on bimorph quality

**Pass Criteria**: Peak thrust > 1 mN (supports ~100 mg flight mass with margin)

---

## 3. IMU Calibration

**Accelerometer**:
1. Place prototype on level surface
2. Record 5-second static sample:
   ```bash
   python phase1/test_procedures.py --log_imu
   ```
3. Calculate bias for each axis:
   - Z-axis should read ~9.81 m/s² (gravity)
   - X, Y should read ~0 m/s²
4. If offset: store calibration_offsets.json with bias values
5. Example:
   ```json
   {"accel_x_bias": 0.05, "accel_y_bias": -0.02, "accel_z_bias": 0.03}
   ```

**Gyroscope**:
1. Place prototype on non-vibrating surface
2. Record 10-second static IMU sample
3. Calculate gyro drift (should be < ±5 deg/sec)
4. If drift excessive: may indicate temperature drift or bent sensor

---

## 4. Center-of-Gravity (CoG) Alignment

**Objective**: Achieve balanced flight (±0.2 mm per spec from Module 05)

**Procedure**:
1. Support prototype on sharp point (pivot) at estimated CoG location
2. Observe tilt direction (forward/backward, left/right)
3. Adjust mass by adding/removing tape or padding:
   - Forward tilt: add mass to rear (tail area)
   - Left tilt: add mass to right wing area
   - Add 0.5–1.0 mg at a time, test balance
4. Repeat until level within ±2 degrees
5. Document final CoG location: measure from body reference point

**Pass Criteria**: Balanced orientation ±2 degrees in all axes

---

## 5. Wing Stroke Symmetry

**Procedure**:
1. Visually inspect wing vibration at 200 Hz:
   - Both wings should move in phase (up-down together)
   - Amplitudes should match (not one wing larger)
2. If asymmetric:
   - Check actuator solder joints (one may be cold)
   - Check wing-actuator epoxy bond (may have gaps)
   - Check for bent/warped wing

**Pass Criteria**: Symmetric vibration, equal amplitudes

---

## 6. Voltage & Current Verification

**Procedure**:
1. Measure at test pads with multimeter (DC):
   - TP1 (+3.3V): 3.25–3.35V ✓
   - TP2 (+5V): 4.9–5.1V ✓
2. Measure current draw:
   - At rest (no PWM): < 50 mA (mostly nRF52 sleep)
   - At 200 Hz, 50% PWM: 200–400 mA (actuator + electronics)
3. If higher: check for short circuit in motor driver or actuator

**Pass Criteria**: Voltages within spec, current < 500 mA at 50% PWM

---

## 7. Thermal Check

**Procedure**:
1. Drive actuators at 50% PWM for 5 minutes
2. Use IR thermometer or thermal camera to measure temperature
3. Check motor driver (DRV8838): should be <50°C
4. Check actuators: should be <40°C
5. If hot: may indicate shorted turns in actuator or excessive current

**Pass Criteria**: Temperature < 50°C (no heatsink needed)

---

## Calibration Data Storage

Save all results to `phase1/calibration_data.json`:

```json
{
  "date": "2026-04-03",
  "wing_resonance_hz": 195,
  "peak_thrust_mg": 1250,
  "imu_accel_bias": {"x": 0.05, "y": -0.02, "z": -0.08},
  "imu_gyro_bias": {"x": 0.2, "y": 0.1, "z": 0.3},
  "cog_position_mm": {"x": 0.1, "y": -0.3, "z": 0.0},
  "voltage_3v3": 3.31,
  "voltage_5v": 5.02,
  "current_idle_ma": 35,
  "current_active_ma": 285,
  "temperature_max_c": 38
}
```

---

**Calibration Complete**: Once all items PASS, prototype is ready for wind tunnel testing (Phase 1 Test Protocol)

