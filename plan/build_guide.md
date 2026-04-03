# Phase 1: Bench Prototype Build Guide

**Objective**: Build a tethered flapping-wing robot to validate simulation  
**Timeline**: 8–12 weeks  
**Budget**: $500–1,500 per robot  
**Difficulty**: Intermediate (mechanical assembly, soldering, debugging)

This guide assumes you've completed Phase 0 simulation and have realistic targets for:
- Wing beat frequency (Hz)
- Stroke amplitude (°)
- Thrust requirement (mN)
- Total mass budget (mg)

---

## Week 1–2: Mechanical Assembly

### 1.1 Wing Fabrication

**Option A: Laser-Cut Carbon Fiber (Recommended)**

Materials:
- Carbon fiber prepreg sheets (0.05 mm, [±45°] ply) — $20/sq ft
- Epoxy resin (two-part, room-temp cure) — $10

Process:
```
1. Design wing profile (2D drawing)
   - Span: 3–4 mm
   - Chord: 1–2 mm
   - Thickness: 0.05 mm
   - Save as .dxf or .pdf

2. Send to laser-cutting service (Ponoko, Epilog, local makerspace)
   - Cost: $50–100 per design
   - Time: 1 week turnaround

3. Receive cut wings (2 pairs minimum for redundancy)

4. Quality check:
   - Measure dimensions (±0.1 mm tolerance)
   - Test for warping (lay flat, check surface)
   - Sand edges smooth (220-grit sandpaper)
```

**Option B: 3D Printed Wings (Faster, Less Stiff)**

Materials:
- Resin (SLA or DLP) — $10–20 per wing
- Or nylon (SLS) — more durable

Process:
```
1. Model wing in FreeCAD (.stl export)

2. Send to 3D printing service (Protolabs, Shapeways)
   - Cost: $20–50 per set
   - Time: 2–3 days

3. Post-process:
   - Cure under UV (if resin)
   - Sand smooth (400-grit)
   - Apply thin epoxy coating if too flexible
```

**Option C: Mylar Film (Fastest, Fragile)**

Materials:
- Mylar sheet (0.03–0.05 mm) — $5
- Adhesive-backed carbon fiber frame or bamboo

Process:
```
1. Laser-cut or hand-cut bamboo frame (2 mm × 0.5 mm)
2. Glue Mylar to frame with spray adhesive
3. Shape to wing profile
Time: 1 day
Cost: $5–10 per wing
Durability: 5–10 flights before tears
```

**Recommendation for first prototype**: Laser-cut carbon fiber (best balance of stiffness, light weight, durability).

---

### 1.2 Body Frame

**3D Print Thorax Structure**

Design considerations:
- Hollow body (minimize mass)
- Wing root attachment: 4–8 mounting points
- Actuator mounting: central cavity
- CoG location: must be within ±0.2 mm of desired location

Material:
- SLA resin (Formlabs, Prusa) — 2–4 mg per body
- Or nylon (Shapeways) — slightly heavier but more durable

Process:
```
1. Model body in FreeCAD or Fusion 360
   - Import wing profile
   - Design cavity for piezo actuator
   - Add mounting holes for electronics
   - Target mass: 2–3 mg (without actuators/electronics)

2. Slice for printing (supports will be needed)

3. Print (local university makerspace or Protolabs)
   - Cost: $50–150
   - Time: 1–3 days

4. Post-process:
   - Dip in IPA (isopropyl alcohol) to dissolve support resin
   - Cure under UV oven (30 min)
   - Sand smooth (1000-grit) if needed
```

**CoG Verification (CRITICAL)**
```
1. Weigh body + wings + actuators
   
2. Use balance beam (or digital scale + precision fixtures):
   - Place robot on razor blade edge (aligned with desired CoG)
   - Does it balance without tipping? If yes, CoG is correct (±0.1 mm)
   - If tips: add 0.5 mg weights (tiny epoxy + lead shot) to lighter side
   - Iterate until balanced
```

---

### 1.3 Actuator Integration

**Off-the-Shelf Piezo Bimorph**

Supplier: Physik Instrumente (PI) or Smart Materials Corp

Spec:
- Length: 10 mm
- Width: 5 mm
- Thickness: 0.8 mm
- Material: PZT-5H (ceramic)
- Capacitance: 100–200 nF
- Max voltage: 30 V (some go to 50 V)
- Blocking force @ 30V: 2–5 mN
- Resonance freq: 800–1500 Hz (well above wing beat)

Cost: $200–400 per pair (2 needed, one per wing)

**Mounting**
```
1. Epoxy actuator to wing root (base of wing)
   - Use aerospace epoxy (3M Scotch-Weld, Loctite E-120HP)
   - Apply thin bead (< 1 mm) to avoid mass penalty
   - Clamp with light pressure (0.5 kg) for 24 hr cure

2. Electrical connection:
   - Solder 0.1 mm copper wire to bimorph pads (or use conductive epoxy)
   - Route wires to electronics board
   - Use conformal coating (silicone) for strain relief
```

**Testing Actuator Response**
```python
# After mounting, verify bimorph oscillates at desired frequency
# Use signal generator + oscilloscope

import numpy as np
import matplotlib.pyplot as plt

# Frequency sweep test:
# - Apply 5 Vpp sine wave at 50 Hz, measure displacement
# - Sweep 50 to 300 Hz
# - Plot amplitude vs. frequency
# - Should show peak at resonance (~1000 Hz) + lower response at wing freq (100-200 Hz)

# Expected plot: small displacement at wing freq (good — no resonance coupling)
```

---

## Week 3–4: Electrical Integration

### 2.1 Motor Driver Circuit

**Simplified Schematic** (wire-tethered version)

```
Signal Generator (external)
        ↓
    Oscilloscope (to monitor)
        ↓
    Amplifier (0–30 V, 1 A output)
        ↓
    [Left Wing] [Right Wing]  (piezo bimorphs in parallel or series)
```

**For wireless**, use:

```
        BLE Module (nRF52832)
              ↓
      H-Bridge Motor Driver (DRV8833 or similar)
              ↓
         PWM to Piezos (1–5 kHz @ 30V)
```

### 2.2 Minimal Tethered Setup (Week 3 Only)

**Cheapest first test** ($50 total):

1. Function generator (e.g., Rigol DG811, $100 used on eBay)
2. Power amplifier (Harrow Electronics PA 2000, $200, or rent from university)
3. Oscilloscope (Rigol DS1054Z, $300 used, or use phone slow-mo camera)
4. Load cell (50 g × 0.01 g precision, $30–50 Amazon)

Process:
```
1. Connect piezo bimorphs to function generator output (start at 5 V, 100 Hz)

2. Attach thin fishing line to robot's wing root

3. Hang from load cell mounted above

4. Measure:
   - Wing motion (camera slow-mo: iPhone, 240 fps)
   - Thrust (load cell reading)
   - Frequency response (function gen sweep 50–300 Hz)
   - Input current (multimeter on signal gen output)

5. Plot:
   - Thrust (mN) vs. frequency (Hz)
   - Compare to simulation prediction
```

**Expected results** (will likely not match simulation):
- Thrust too low? Wings too flexible, or epoxy joint is failing
- Wings not beating? Actuator not bonded, or driving voltage too low
- Asymmetry? CoG off-center, or one actuator weaker

---

### 2.3 Full Wireless Version (Week 4)

**BLE-Based Control**

Components:
- MCU: STM32L151 (ultra-low power)
- BLE radio: nRF52832 (integrate with STM32 or use separate module)
- Motor driver: DRV8833 (dual H-bridge, 3.3V logic)
- PWM DAC: AD5754 (16-bit, convert digital PWM to analog voltage)

Schematic (text):
```
Smartphone BLE app
        ↓
   nRF52832 (5 pins: GND, VCC, TX, RX, PWM)
        ↓
   STM32L151 (runs PID loop, 500 Hz update)
        ↓
   DRV8833 (dual H-bridge: left wing, right wing)
        ↓
   High-voltage amplifier → Piezos
```

PCB layout (simple):
- 2-layer board, 10 cm × 5 cm
- Get manufactured at JLCPCB ($20–30)

Firmware (pseudocode):
```c
// STM32 main loop
while (1) {
    // Receive BLE command (left freq, right freq, amplitude)
    
    // Update PWM for each wing:
    // left_pwm = sin(2*pi*freq_left*t) * amplitude
    // right_pwm = sin(2*pi*freq_right*t + pi) * amplitude  // 180° phase offset
    
    // Output 30V through DAC and amplifier
    
    // Read IMU (9-DOF: accel, gyro, mag)
    // optional: PID feedback loop
    
    // Repeat at 500 Hz
}
```

---

## Week 5–6: Tether & Ground Test

### 3.1 Load Cell Setup

**Static Thrust Measurement**

```
Aluminum stand (aluminum extrusion, $50)
        ↓
    Load cell (50 g, precision ±0.01 g)
        ↓
    Thin monofilament (0.3 mm fishing line)
        ↓
    Robot (tethered)
        ↓
    Function generator (or wireless control)
```

**Measurement Protocol**

```python
# Pseudocode for thrust vs. frequency test

import numpy as np
import matplotlib.pyplot as plt

frequencies = np.linspace(50, 300, 50)  # Hz
thrusts = []

for freq in frequencies:
    # Set function gen to this frequency, 30 Vpp amplitude
    input("Press ENTER when ready...")
    
    # Read load cell 10 times, average
    readings = [scale.read() for _ in range(10)]
    thrust_mg = np.mean(readings)
    thrusts.append(thrust_mg)
    
    print(f"{freq} Hz → {thrust_mg:.2f} mg thrust")

# Plot
plt.figure()
plt.plot(frequencies, thrusts, 'o-', linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Thrust (mg)')
plt.title('Thrust vs. Frequency')
plt.grid()
plt.savefig('thrust_curve.png', dpi=150)
plt.show()

# Calculate figure of merit
robot_mass_mg = 8  # your robot weight
thrust_at_flight_freq = 15  # interpolate from data
thrust_to_weight = thrust_at_flight_freq / robot_mass_mg
print(f"Thrust/weight ratio: {thrust_to_weight:.2f}")
# Should be > 1.5 for stable flight
```

**Common Issues & Fixes**

| Problem | Symptom | Fix |
|---|---|---|
| Wings not moving | No thrust at any frequency | Check epoxy bond (gently tug wing — should not move) |
| Low thrust | T/W < 1.0 | Increase voltage (30V max), or stiffer wings, or larger actuator |
| Noisy readings | Thrust jumps ±10 mg | Add damping (check load cell mounting bolts), average more readings |
| Resonance peak | Sharp T spike at one frequency | Expected! (actuator resonance ~1000 Hz). Avoid that frequency. |
| Frequency response strange | Not smooth curve | Check wing bond, balance CoG |

---

## Week 7–8: Dynamic Flight Test

### 4.1 Wind Tunnel or Large Room

**Setup**
- Clear 2 m × 2 m × 2 m space (classroom, gym, hangar)
- Monofilament tether (0.5 m long, attached to overhead beam)
- Smartphone slow-mo camera (iPhone 13+, 240 fps)
- IMU on robot (9-DOF, log to onboard SD card)

**Flight Test Protocol**

```python
import cv2  # For video analysis
import numpy as np

# Slow-motion video (240 fps, 30 sec = 7200 frames)

# Manually mark wing positions in first/last frames of each flap
# Calculate: wing displacement, frequency, symmetry

# From IMU data:
# - Roll/pitch rates (dψ/dt should be < 10 deg/s for stable hover)
# - Accelerometer (should average ≈ 9.8 m/s² downward if hovering)

# Run test:
# 1. Enable wireless control
# 2. Set wing freq = target (from simulation)
# 3. Increase amplitude gradually until robot lifts off tether slack
# 4. Record video + IMU
# 5. Land and analyze

# Results to compare with simulation:
# - Actual wing beat frequency vs. command frequency
# - Actual thrust vs. simulated thrust
# - Control authority (roll/pitch rates per actuator imbalance)
# - Power draw (estimate from input current × voltage)
```

**Expected Outcome**

If simulation was correct:
- ✓ Robot hovers at predicted frequency
- ✓ Thrust/weight ratio matches
- ✓ Control feels responsive (< 100 ms lag)

If not (most likely):
- ✗ Thrust 50% lower than expected
  - Why: wing flex, dead-band in motor driver, epoxy not fully cured
  - Fix: increase voltage to 50V (if actuator supports), or stiffer wings
  
- ✗ Frequency response shifted
  - Why: resonance mismatch, damping higher than predicted
  - Fix: adjust simulation damping, re-run control design

- ✗ Control instability (oscillations)
  - Why: phase margin too low, wireless latency
  - Fix: reduce PID gains, lower update rate if wireless is laggy

---

## Week 9–10: Wireless & Iteration

### 5.1 Remove Tether (Carefully)

```
1. Reduce monofilament diameter gradually:
   - 0.5 mm (5 flights)
   - 0.3 mm (5 flights)
   - 0.1 mm (monofilament, can't support weight but catches if needed)
   - Remove entirely

2. First free flight:
   - Start in enclosed space (no wind)
   - Short flight (5 sec) → land
   - Repeat with longer flights as confidence builds
   - Have safety net or catch box ready
```

### 5.2 Refinement

Based on tethered vs. free flight, iterate:

| Observation | Change |
|---|---|
| Drifts to one side | Adjust wing amplitude asymmetry (PID yaw controller) |
| Dives or climbs slowly | Adjust hover amplitude (increase/decrease pitch offset) |
| Falls like a rock | Not enough thrust — redesign needed (Phase 0 sim was wrong) |
| Oscillates (Dutch roll) | Reduce bandwidth, increase damping in PID |
| Battery depletes in 5 min | Higher power draw than expected — adjust wing frequency or use larger battery |

---

## Bill of Materials (Phase 1 Build)

| Item | Cost | Supplier | Notes |
|---|---|---|---|
| **Structural** |
| Carbon fiber wings (laser-cut) | $100 | Ponoko / Epilog | 2 sets for redundancy |
| 3D printed body | $100 | Protolabs / Formlabs | SLA resin |
| Epoxy adhesive (aerospace) | $15 | Home Depot / McMaster | 3M Scotch-Weld |
| **Actuation** |
| PZT bimorph actuators (pair) | $300 | Physik Instrumente | 10×5 mm, 30V |
| Copper wire (0.1 mm) | $5 | Amazon | For wiring |
| **Electronics** |
| STM32L151 dev board | $15 | eBay / ST | Or custom PCB |
| nRF52832 BLE module | $20 | Adafruit | Pre-assembled module |
| DRV8833 motor driver IC | $5 | Digikey | Dual H-bridge |
| Operational amplifiers | $5 | Digikey | For signal conditioning |
| Resistors, capacitors, headers | $20 | JLCPCB, Digikey | Standard passive BOM |
| Custom PCB (2-layer, 100 mm) | $30 | JLCPCB | 5 units minimum |
| Connectors, headers, solder | $15 | Digikey | Standard assembly supplies |
| **Power** |
| Li-polymer battery (50 mAh, 3.7V) | $15 | Tadiran / Tenergy | Smallest practical |
| Battery charger | $10 | Adafruit | USB micro charging |
| **Test Equipment** |
| Load cell (50 g, USB) | $40 | Amazon / Verifone | For static thrust test |
| Function generator | $100–200 | Used eBay | Or borrow from university |
| Oscilloscope | $200–300 | Used eBay | Or use smartphone slow-mo camera |
| **Miscellaneous** |
| Fishing line, epo xy, sandpaper | $30 | Hardware store | Assembly supplies |
| Aluminum extrusion, fasteners | $50 | McMaster, local | Tether rig |

---

## Timeline & Checkpoint

| Week | Task | Go/No-Go |
|---|---|---|
| 1–2 | Wings + Body | Weigh < 5 mg? Balanced? |
| 3–4 | Actuator integration | Bimorph bonded & tested? |
| 5–6 | Static thrust test | T/W ≥ 1.5 at target frequency? |
| 7–8 | Tethered dynamic test | Wings beat at expected frequency? |
| 9–10 | Free flight | Hovers stably? |

**If any checkpoint fails**: Do not proceed to next week. Debug and re-test.

---

## Success Criteria

After Phase 1, you should be able to:

- [ ] Hover robot for > 5 seconds indoors
- [ ] Control pitch/roll via wireless command
- [ ] Measure thrust and compare to simulation (within ±30%)
- [ ] Understand where simulation was wrong (and fix it)
- [ ] Have realistic specifications for Phase 2 MEMS design

If all above → proceed to Phase 2 (MEMS fabrication)  
If any fail → stay in Phase 0, refine simulation further

---

## Reference: MIT RoboBees Lessons Learned

From publications:
1. **Wing bonding is critical** — use aerospace epoxy, not superglue
2. **Power consumption scales as (mass)^(1/2)** — lighter is harder
3. **Control latency must be < 50 ms** — wireless adds 20–30 ms delay
4. **First prototype always needs iteration** — expect 3–5 design cycles
5. **Allan deviation matters** — frequency stability for autonomous flight
6. **Manufacturing tolerances kill you** — ±0.1 mm asymmetry causes roll bias

---

## Next Steps

1. Read **ROADMAP.md** for full context
2. Gather Phase 1 budget ($500–1000)
3. Run Phase 0 simulation to predict critical specs
4. Order components (parallel with Wing/Body fabrication)
5. Start Week 1 mechanical assembly

Good luck! 🚁
