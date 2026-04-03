# Professional Pipeline: Simulation → Build for Flapping-Wing Microrobots

**Target**: Autonomous flying microrobot (5–50 mg), flapping-wing design inspired by Drosophila  
**Timeline**: Phase 0 (simulation): 3–6 months | Phase 1 (prototype): 2–3 months | Phase 2 (MEMS): 6–12 months  
**Budget**: Phase 0: ~$5k (compute + software) | Phase 1: ~$20k (actuators, components, test rig) | Phase 2: ~$100k+ (foundry, tooling)

---

## Phase 0: Simulation (You Are Here)

### A. Why Simulation Matters at This Scale

Standard aerodynamic textbooks are **wrong for insects**.

| Flight Regime | Reynolds # | Lift Model | Your Drone |
|---|---|---|---|
| Commercial jets | 10^6 | Attached flow, thin airfoil theory | ✗ |
| **Small insects (Drosophila)** | **100–1,000** | **Leading-edge vortex (LEV), rotational lift** | **✓ THIS IS YOU** |
| Hummingbirds | 1,000–10,000 | Transitional (LEV fades) | ✗ |

**Key insight**: At your Reynolds number, wings generate lift *not because they're shaped like airfoils*, but because they punch a vortex into the fluid every stroke. This is called the "leading-edge vortex" mechanism.

**Consequence**: Quasi-steady models underpredict lift by 20–40%. You must either:
1. Use empirical unsteady force models (Dickinson et al., Whitney & Wood)
2. Run CFD (OpenFOAM)
3. Combine both (model + CFD validation)

---

### B. Simulation Stack

Choose one of three paths based on your time/accuracy tradeoff:

#### **Path A: Fast (Recommended to Start)**
Fast Python-only, 80% accurate, runs in seconds.

```
Module 00 (biomechanics)
    ↓
Module 01 (actuator)
    ↓
Module 02 (aero: Whitney & Wood quasi-static model)
    ↓
Module 06 (control: python-control, Bode plots)
    ↓
Module 09 (integration)
```

**Tools**:
- Python 3.9+
- NumPy, SciPy, Matplotlib
- `python-control` (Bode, stability analysis)
- `allantools` (if studying Allan deviation)

**Accuracy**: Thrust/weight ratio ±15%, control bandwidth ±10%

---

#### **Path B: Validation (Medium)**
Fast model + selective CFD runs, 90% accurate, runs in hours/days.

```
Path A (above)
    +
OpenFOAM (wing aero verification at 1–2 flight conditions)
    +
XFOIL (generate 2D airfoil polars for different Re)
    ↓
Refine Whitney & Wood model with CFD corrections
```

**Additional Tools**:
- OpenFOAM (free, open-source CFD)
- XFOIL (inviscid airfoil analysis)
- Salome (meshing)
- ParaView (visualization)

**Accuracy**: ±5–10%

**Timeline**: 4–8 weeks for one wing configuration

---

#### **Path C: Detailed (Slow)**
Full CFD + FEM + co-simulation, 95%+ accurate, runs in weeks.

```
Path B (above)
    +
Elmer FEM (wing structure, modes, stress)
    +
MuJoCo (multi-body dynamics)
    +
FSI coupling (wing flex → aero feedback)
    ↓
End-to-end co-simulation
```

**Additional Tools**:
- Elmer (free FEM solver)
- MuJoCo (rigid+compliant dynamics, free academic license)
- Python glue (scipy.integrate.odeint for coupling)

**Accuracy**: 95%+

**Timeline**: 3–6 months for one design cycle

---

### C. Phase 0 Deliverables

After simulation, you should have:

1. **Thrust polars**: Thrust (mN) vs. frequency (Hz) and stroke amplitude (°)
2. **Power budget**: Total power (mW) split by actuator, electronics, sensors
3. **Flight envelope**: Max speed, max acceleration, stability margins
4. **Control design**: PID gains, bandwidth (Hz), phase/gain margins
5. **Validation gaps**: Where simulation doesn't match literature or where CFD is needed

---

## Phase 1: Bench Prototype (No Clean Room)

Build a tethered flyer to validate simulation predictions. **This is critical** — simulation is wrong. You will learn by comparing sim vs. hardware.

### A. Component Sourcing

| Component | Spec | Supplier | Cost | Notes |
|---|---|---|---|---|
| **Piezo bimorph actuator** | 2×10mm, 30V, 1–5 mN force | Physik Instrumente (PA4FE) or Smart Materials | $200–400/pair | Off-the-shelf, characterized |
| **Wings** | 3mm span, 0.05mm carbon fiber | Laser-cut locally (epilog.com) or handmade | $100–300 | Prepreg carbon, ply [\deg0/45/-45/0] |
| **Body frame** | 2–3 mg, balsa wood or 3D resin | 3D print (SLA), then lighten | $50–150 | SLA resin prints in 1 day |
| **MCU + wireless** | STM32L0 + nRF52 BLE | Adafruit Feather or custom PCB | $30–80 | Or: wire-tethered first (no wireless) |
| **IMU / AHRS** | 6-DOF accel+gyro | ICM-20602 or MPU-6050 | $10–20 | For attitude feedback |
| **Li-poly battery** | 50 mAh @ 3.7V | Tenergy Tadiran | $10–20 | ~10 min flight time |
| **Custom PCB** | Signal conditioning, motor driver | JLCPCB or OSH Park | $20–50 | Simple 2-layer board |

**Total Phase 1 BOM**: $420–1,000 per robot

### B. Build Process

1. **Weeks 1–2: Mechanical assembly**
   - 3D print body
   - Laser-cut wings
   - Glue actuators to wing roots (epoxy: use servo control adhesive)
   - Wire everything together with 0.05 mm copper wire
   - Balance: CoG < 0.2 mm from centerline (critical!)

2. **Weeks 3–4: Electrical integration**
   - Solder STM32 + BLE module on custom PCB
   - Add motor driver (H-bridge for PWM to piezo)
   - Integrate IMU
   - Battery connector + charging circuit

3. **Weeks 5: Tethering & Ground Test**
   - Attach thin monofilament (fishing line) from robot body to force sensor
   - Static test: measure thrust vs. input voltage
   - Compare to simulation

4. **Weeks 6–8: Dynamic Flight Test**
   - Hang from load cell (measure vertical force)
   - Visual tracking (iPhone slow-mo at 240 fps)
   - Measure wing beat frequency with accelerometer FFT
   - Iterate on wing stiffness, actuator tuning

5. **Weeks 9–10: Wireless & Flight**
   - If hardware works, add wireless control
   - Tether still on (safety)
   - First free flight indoors (wind tunnel or large room)

### C. Expected Outcomes

**What you'll learn**:
- Does your simulation predict thrust correctly? (Usually off by 50% first time)
- What breaks first? (Glue joints, wing fatigue, battery life)
- Can you actually balance & control a 5 mg flying robot? (Harder than simulation)

**What might go wrong**:
- Wings too stiff/too flexible (tuning nightmare)
- Actuator can't provide enough force (redesign needed)
- Payload of MCU + battery too heavy (go tethered only)
- Aerodynamic flutter (structural resonance issue)

**Timeline**: 8–12 weeks, depending on iteration loops

---

## Phase 2: MEMS Fabrication

Once Phase 1 prototype validates your design, you go to a MEMS foundry.

### A. Foundry Options

| Foundry | Process | Lead Time | Cost | Access |
|---|---|---|---|---|
| **MEMS+ / SiTime** | SiGe, CMOS-MEMS | 16 weeks | $50k–200k | Industry (licensing) |
| **Sandia SUMMIT V** | Multi-layer polysilicon | 8 weeks | $30k–100k | US gov/universities |
| **MIT.nano / Stanford SNF** | Academic access to industry tools | 4–8 weeks | $500–2k labor | University affiliates |
| **China (Akhan, ASE)** | RF MEMS, custom co-process | 12 weeks | $20k–80k | Anyone (lead time risk) |

### B. What Gets Made

Integrate at MEMS scale:

1. **Body**: Silicon etched to shape (500 µm, high Q resonance)
2. **Actuators**: PZT thin film or MEMS piezo on top
3. **Wings**: Silicon nitride (very light, high stiffness)
4. **Electronics**: Monolithic or bonded (IC on silicon)

**Design rules** (what you must know):
- Minimum feature: 2–5 µm (depends on foundry)
- Aspect ratio: depth/width < 10–20:1 (limits tall structures)
- Stress limits: use σ_max < 100 MPa (avoid fracture)
- Thermal budget: max 200–400°C (don't melt sacrificial layers)

### C. Design Specification → Fabrication

Before you send design to foundry:

1. **Design Rule Deck** (DRD)
   - Layer stack: which layers, thicknesses, spacing
   - Minimum features, spacing rules
   - Etch depth targets

2. **Layout (GDS-II)**
   - All patterns in GDSII format
   - Layer assignments (layer numbers, datatype)
   - Design rule checking (DRC) passed

3. **Process Traveler** (detailed fab instructions)
   - Material specs (dopant levels, oxide thickness, etc.)
   - Etch recipes (DRIE pressure, time, chemistry)
   - Bonding/assembly steps

4. **Verification Plan**
   - SEM cross-sections at key points
   - Resonance frequency measurement (must hit target ±5%)
   - Stress verification (optical inspection, may include strain gauge)

### D. Timeline & Costs

| Phase | Task | Time | Cost |
|---|---|---|---|
| 0a | Design capture (CAD → GDS) | 4 weeks | $0 (in-house) |
| 0b | DFM review with foundry | 2 weeks | $2k–5k (foundry engineering) |
| 1 | Mask tooling | 4 weeks | $10k–30k (photo masks) |
| 2 | Wafer run | 8 weeks | $15k–50k (wafer cost + processing) |
| 3 | Dicing + QA | 2 weeks | $2k–5k |
| 4 | Your assembly + test | 4 weeks | $5k–10k (labor) |

**Total**: $34k–100k, 20 weeks

---

## Path Recommendation: Phase 0 → Phase 1 → Phase 2

1. **Now**: Run Path A simulation (8 weeks, $0 software cost)
   - Get realistic aerodynamic numbers
   - Design control loop
   - Identify critical specs (wing stiffness, actuator force, etc.)

2. **Months 3–5**: Build Phase 1 bench prototype (12 weeks)
   - Validate simulation vs. hardware
   - Find unknowns (e.g., wing fatigue, balance difficulty)
   - Refine mechanical design

3. **Months 6–8**: Design iteration + CFD validation (Path B, 8 weeks)
   - Run OpenFOAM on final wing design
   - Compare to Whitney & Wood model
   - Finalize process spec for foundry

4. **Months 9–14**: MEMS fabrication (Phase 2, 20 weeks)
   - Send GDS + process traveler to foundry
   - First wafer run
   - Test, iterate

---

## Key References (Implement These in Simulation)

| Paper | What | How to Use |
|---|---|---|
| Dickinson et al. (2000) *J. Exp. Biol.* | Unsteady lift, drag, torque for insect wings | Python: add LEV correction factor to quasi-steady model |
| Whitney & Wood (2010) *Bioinsp. Biomim.* | Quasi-static flapping model for RoboBees | Implement full equations: L, D vs. φ (stroke), φ̇ (rate) |
| Lentink & Dickinson (2009) | Rotational lift mechanism | Use empirical correction: +30% lift during rotation |
| Combes & Dudley (2002) *Nature* | Stability limits, turbulence effects | Identify control bandwidth requirement |
| Tanaka et al. (2013) *IJMSM* | Piezo actuator scaling, PZT properties | Use force-displacement curves for phase 1 prototype |

---

## Checkpoint Questions Before Starting Phase 1

Before you spend money, verify simulation predicts:

- [ ] Thrust/weight ratio ≥ 1.5 (need margin for control)
- [ ] Wing beat frequency matches biologically plausible actuator (50–200 Hz)
- [ ] Power budget < 100 mW (battery feasible)
- [ ] Control bandwidth > 20 Hz (stable attitude loop possible)
- [ ] Wing resonance > 2× beat frequency (avoid aeroelastic flutter)

If all checkboxes pass → Phase 1 is worth building  
If any fail → redesign in simulation first

---

## Next Steps

1. Read `tools_guide.md` for installation instructions
2. Run `robotic-insects/evaluate_all.py` to see current status
3. Start with `02_wing_aerodynamics/sim.py` (most critical)
4. Compare your output against Dickinson & Whitney & Wood numbers in literature
