# Phase 1: Assembly Procedure — RoboInsect v1.0

**Target Build Time**: 8–10 hours for first prototype  
**Tools Required**: Soldering iron (25W), tweezers, hot air station, wire cutters, precision scale, oscilloscope  
**Safety**: ESD wrist strap, lead-free solder, fume extractor, eye protection  

---

## PHASE 1: PCB FABRICATION & ELECTRONICS

### Step 1.1: Order PCB from JLCPCB
- Export Gerber files from KiCad schematic
- Order 5-unit batch: 2-layer FR4, 1.6 mm thickness, HASL finish
- Lead time: 5–7 days
- Cost: ~$8 for 5 boards
- **Checklist**: ☐ Gerbers uploaded ☐ Quote accepted ☐ Order placed ☐ Tracking #___

### Step 1.2: Prep PCB for Assembly
1. Inspect PCB for defects (cracks, solder bridges, shorts)
2. Clean with IPA (isopropyl alcohol) and lint-free cloth
3. Apply solder paste (no-clean, lead-free) to all pads using stencil or syringe
4. Let paste cure 30 min at room temperature (do not refrigerate — paste loses activity)
5. **Checklist**: ☐ PCB inspected ☐ Paste applied evenly ☐ 30 min wait done

### Step 1.3: Place SMD Components
Using tweezers and solder paste:
1. Place capacitors (C1–C8): 0603 ceramic and tantalum
2. Place resistors: 0.22Ω sense, 4.7k pull-ups
3. Place ICs: DRV8838 (×2, SOIC-8), MCP6001 (DIP-8)
4. Place diode D1 (SS14 Schottky) — observe polarity (cathode marked)
5. Place test pads (TP1–TP7): vias with 0.125" header pin stubs
6. **Checklist**: ☐ All parts placed ☐ Orientation verified ☐ Paste not bridging

### Step 1.4: Reflow Soldering
**Hot air station profile** (lead-free SnPb solder):
- Preheat: 160°C, 60–90 seconds
- Ramp: 3°C/sec to peak (245°C)
- Dwell: 245°C, 10–30 seconds
- Reflow: 245°C, 5–10 seconds
- Cool: <2°C/sec to room temp

**Process**:
1. Load PCB on stainless steel carrier
2. Place nozzle 5 cm above PCB, apply hot air at 300 mL/min
3. Watch for solder to flow and reflow all pads
4. Remove from hot air, cool 2 minutes
5. Inspect for cold solder joints (grainy, dull appearance) — reflow if found
6. **Checklist**: ☐ Profile followed ☐ All solder shiny ☐ No bridges

### Step 1.5: Hand-Solder Header Connector
1. Insert 2×5 header (J1) through holes
2. Solder from backside (ground plane side) using 25W iron
3. Use flux-core solder, wet the pad first, then heat both pad and pin
4. Inspect: solder should fillet around pin (volcano shape, not blob)
5. **Checklist**: ☐ Header installed ☐ All pins wetted ☐ No cold joints

### Step 1.6: Test Continuity
Using multimeter (ohms mode):
1. Test GND plane (all ground pads connected)
2. Test +3.3V rail (no shorts to GND)
3. Test +5V rail (no shorts to GND)
4. Test signal lines (no opens)
5. **Checklist**: ☐ All continuity tests passed ☐ No shorts detected

---

## PHASE 2: nRF52810 DK INTEGRATION

### Step 2.1: Connect nRF52 Dev Board
1. Connect nRF52810 DK to PCB via J1 header using 6" jumper wires:
   - nRF P0.13 → PCB P0.13 (PWM1)
   - nRF P0.14 → PCB P0.14 (PWM2)
   - nRF P0.15 → PCB P0.15 (DIR1)
   - nRF P0.16 → PCB P0.16 (DIR2)
   - nRF P0.17 → PCB P0.17 (SDA)
   - nRF P0.18 → PCB P0.18 (SCL)
   - nRF P0.19 → PCB P0.19 (AREF)
   - nRF GND → PCB GND (×2)
   - nRF +3.3V → PCB +3.3V
2. **Checklist**: ☐ All connections made ☐ No shorts ☐ Wires strain-relieved

### Step 2.2: Program nRF52
1. Download nRF SDK from Nordic Semiconductor
2. Flash bootloader using SWD interface (openocd or nRFgo):
   ```bash
   openocd -f nrf52810.cfg -c "program bootloader.hex reset"
   ```
3. Upload test firmware (blink LED to verify):
   ```bash
   openocd -f nrf52810.cfg -c "program firmware.hex reset"
   ```
4. Check serial output (115200 baud): should see startup message
5. **Checklist**: ☐ Bootloader flashed ☐ Test FW loaded ☐ Serial OK

### Step 2.3: First Power-On Test
1. Connect USB battery charger to TP2 (+5V) and TP3 (GND)
2. Measure voltages on test pads:
   - TP1 (+3.3V): should read 3.25–3.35V
   - TP2 (+5V): should read 4.9–5.1V
   - TP3 (GND): should read 0V
3. If voltages wrong:
   - Check LM3671 regulator: may be missing or cold solder
   - Check capacitors C1–C3 for shorts
   - **DO NOT PROCEED** if voltages out of spec
4. **Checklist**: ☐ All voltages correct ☐ No shorts ☐ Ready for sensors

---

## PHASE 3: SENSOR INTEGRATION

### Step 3.1: Connect IMU (ICM-42688)
1. I2C address of ICM-42688: 0x68 (default)
2. Connect breakout to PCB:
   - GND → TP3 (GND)
   - +3.3V → TP1 (+3.3V)
   - SDA → P0.17 (via J1 and jumper)
   - SCL → P0.18 (via J1 and jumper)
3. Load firmware with I2C scanning code:
   ```c
   uint32_t err_code = nrfx_twi_rx(address, data, length);
   ```
4. Run I2C scan: should detect device at 0x68
5. **Checklist**: ☐ Connections verified ☐ I2C scan OK ☐ IMU responsive

### Step 3.2: Calibrate Load Cell (Optional)
1. If using Futek LSB200 load cell:
   - Connect analog output to nRF ADC via op-amp (on PCB)
   - Place known weights (10g, 20g, 50g) on cell
   - Record ADC readings for each weight
   - Store calibration: `ADC_per_gram = (ADC_50g - ADC_0g) / 50`
2. **Checklist**: ☐ Calibration data recorded ☐ Linearity verified (R² > 0.99)

---

## PHASE 4: ACTUATOR ASSEMBLY

### Step 4.1: Prepare PZT Bimorphs
1. Receive 2× PZT-5H bimorph benders from PI or ThorLabs
2. Inspect for cracks or visible damage
3. Measure dimensions: should be 10×5×0.8 mm
4. Clean with dry cloth (do NOT wet — piezo is hygroscopic)
5. **Checklist**: ☐ Both bimorphs intact ☐ Dimensions verified

### Step 4.2: Prepare Carbon Fiber Wings
1. Cut CF sheet 0.1 mm thick into 3×1 mm rectangles (×2 for left/right)
2. Sand edges smooth (220-grit sandpaper)
3. Clean with IPA
4. Dry at 60°C for 2 hours (removes moisture)
5. **Checklist**: ☐ Wings cut to size ☐ Edges smooth ☐ Dried

### Step 4.3: Epoxy Bonding of PZT to Wing
1. Mix 3M DP460 UV epoxy (2-part, 1:1 ratio by volume)
2. Apply thin bead (~0.5 mm) to bottom surface of each bimorph
3. Position bimorph on CF wing using alignment jig:
   - Bimorph centered on wing span
   - Clamp pressure: 1–2 kgf (light, to avoid piezo fracture)
   - Keep clamp time: 30 min (initial set)
4. Expose to UV lamp (365 nm, 40W) for 3 minutes
5. Remove clamp, cure 24 hours at room temperature
6. Check bond: try to lift actuator — should not separate
7. **Checklist**: ☐ Both wings bonded ☐ UV cured ☐ Bond strength OK

---

## PHASE 5: ELECTRICAL INTEGRATION

### Step 5.1: Motor Driver Test
1. Load firmware with PWM output test:
   ```c
   nrfx_pwm_config_t pwm_config = {
     .output_pins = {P0_13, P0_14, P0_15, P0_16},
     .frequency = 1000,  // 1 kHz
     .top_value = 255
   };
   ```
2. Set PWM: 50% duty cycle, 1 kHz
3. Connect oscilloscope to test pads TP4, TP5 (sense voltages)
4. Measure: should see 1 kHz square wave, 0–3.3V amplitude
5. **Checklist**: ☐ PWM signals present ☐ Frequency correct ☐ Amplitude OK

### Step 5.2: Connect PZT Wings to Motor Drivers
1. **Wiring** (magnet wire 28 AWG, soldered to bimorph contacts and DRV8838):
   - Actuator 1+ → DRV8838-1 OUT1
   - Actuator 1- → DRV8838-1 OUT2 (sense resistor here)
   - Actuator 2+ → DRV8838-2 OUT1
   - Actuator 2- → DRV8838-2 OUT2 (sense resistor here)
2. Solder connections (1–2 seconds contact, minimize heat to piezo)
3. Use heat-shrink tubing to insulate solder joints
4. **Checklist**: ☐ All connections soldered ☐ Insulation applied ☐ No shorts

### Step 5.3: First Vibration Test
1. Apply 20V DC to battery input (or USB charger)
2. Program firmware to drive Actuator 1 at 100 Hz (50% duty):
   ```c
   nrfx_pwm_simple_playback(&pwm, 1, false, 255 / 2);
   ```
3. Watch wing: should vibrate at 100 Hz (visible oscillation)
4. Listen: should hear low-frequency hum
5. Feel (gently): vibration should be smooth, symmetric
6. If no vibration:
   - Check solder joint on bimorph contact
   - Check DRV8838 output voltage (should swing 0–5V at 1 kHz)
   - Verify PWM signal on oscilloscope
7. **Checklist**: ☐ Wing 1 vibrates at 100 Hz ☐ Wing 2 vibrates ☐ Smooth motion

---

## PHASE 6: SYSTEM TEST & CALIBRATION

### Step 6.1: Run Test Procedures Script
```bash
python phase1/test_procedures.py --log_imu --log_thrust --sweep 50 300
```
This will:
1. Record IMU (accel, gyro) at 1 kHz for 10 seconds
2. Record load cell thrust as actuator frequency sweeps 50–300 Hz
3. Save CSV file with timestamped data
4. Generate PNG plots of thrust vs. frequency, IMU response

### Step 6.2: Review Results
1. Thrust vs. frequency plot:
   - Should show peak thrust somewhere 150–250 Hz
   - Target: >1 mN peak at design frequency (200 Hz)
2. IMU response:
   - Should correlate with wing frequency
   - Check for anomalies (spikes, noise)
3. If results poor:
   - Increase PZT drive voltage to 25V (within rated limits)
   - Check wing-actuator bond (may be partially delaminated)
4. **Checklist**: ☐ Script ran successfully ☐ Data saved to CSV ☐ Plots reviewed

### Step 6.3: Calibrate Control Law
1. Adjust PWM duty cycle vs. desired thrust using lookup table
2. Tune PID gains (if closed-loop control desired):
   - Start with Kp = 1, Ki = 0, Kd = 0
   - Gradually increase Kp until oscillation appears
   - Add Ki to eliminate steady-state error
   - Add Kd if oscillation persists
3. Store calibration in firmware EEPROM
4. **Checklist**: ☐ Thrust mapping created ☐ PID tuned ☐ Stored in EEPROM

---

## FINAL ASSEMBLY CHECKLIST

- ☐ Phase 1: PCB fabrication & electronics (all steps)
- ☐ Phase 2: nRF52 integration & test (all steps)
- ☐ Phase 3: Sensor integration (all steps)
- ☐ Phase 4: Actuator assembly (all steps)
- ☐ Phase 5: Electrical integration (all steps)
- ☐ Phase 6: System test (all steps)
- ☐ Document all calibration values in `phase1/calibration_data.json`
- ☐ Record video of wing vibration @ 200 Hz
- ☐ Take photos of completed prototype for project documentation

---

**Total Build Time**: 8–10 hours first prototype  
**Estimated Cost**: ~$355 (see BOM)  
**Next Step**: Wind tunnel test (Phase 1 Test Protocol)

---

**Document Version**: v1.0 (2026-04-03)  
**Last Reviewed**: TBD  
**Assembly Lead**: TBD

