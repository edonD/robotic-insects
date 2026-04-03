# START HERE — Professional Robotic Insects Pipeline

**This is your roadmap from simulation to buildable hardware.**

---

## What You Have

A complete professional design framework for **flapping-wing microrobots** (5–50 mg flying robots):

```
robotic-insects/
├── Simulation modules (00–09) ← upgrades with real physics
├── Plan documents (plan/*.md)  ← professional guides
└── Evaluation system           ← strict go/no-go gates
```

---

## What This Means

**Phase 0 (Simulation)**
- Run Python modules to predict thrust, power, control stability
- Models: Whitney & Wood (wing aero), Dickinson (unsteady effects), PID control
- Cost: $0 (everything is free software)
- Timeline: 1–4 weeks
- Accuracy: ±50% on first try (normal!)

**Phase 1 (Bench Prototype)**  
- Build a tethered robot with off-the-shelf parts (PZT actuators, 3D printed body)
- Test in wind tunnel / indoor space
- Compare hardware to simulation (find where sim was wrong)
- Cost: $500–1,500
- Timeline: 8–12 weeks
- Outcome: Flying robot (5+ seconds hover)

**Phase 2 (MEMS)**
- Send design to foundry (Sandia, Stanford, academic, or commercial)
- Integrate chip, actuators, electronics into microfabricated body
- Cost: $100k+
- Timeline: 20 weeks
- Outcome: Manufacturable design

---

## Right Now (Today) — 30 Minutes

### 1. Read This Quick Summary

The three professional guides in `plan/`:

| File | Length | What | For Who |
|---|---|---|---|
| **ROADMAP.md** | 10 min | Full pipeline: simulation → Phase 1 → Phase 2 | Everyone |
| **tools_guide.md** | 5 min | What to install and why | Coders |
| **build_guide.md** | 15 min | How to build Phase 1 prototype step-by-step | Builders |

**Minimum**: Read ROADMAP.md (pages: "Phase 0: Simulation" through "Key References")

### 2. Install Software (5 minutes)

```bash
pip install numpy scipy matplotlib python-control
```

**Verify**:
```bash
python -c "import numpy, scipy, matplotlib, control; print('✓ OK')"
```

### 3. Run the Most Important Simulation (2 minutes)

```bash
cd robotic-insects/
python 02_wing_aerodynamics/sim.py
```

**Look for output**:
```
Thrust at design point: 0.012 mN
Body weight: 0.008 mN
Thrust-to-weight ratio: 1.50

Plots saved: 02_wing_aerodynamics/thrust_vs_frequency.png
```

**Check**: Is T/W > 1.0? (you need margin for control)

---

## This Week — Understanding Phase 0

### Read All 3 Plan Documents

**ROADMAP.md** (10 min read)
- Why insect-scale aerodynamics is different (Reynolds number, leading-edge vortex)
- Three simulation paths (fast Python / medium CFD / slow detailed)
- What Phase 1 build will teach you (simulation is usually wrong)
- Phase 2 MEMS foundry options & costs

**tools_guide.md** (5 min read)
- Tier 1: Python only (do this now) ← You Are Here
- Tier 2: OpenFOAM + XFOIL (if Phase 0 sim is suspicious)
- Tier 3: Elmer FEM + MuJoCo (research-grade, optional)
- Tier 4: FEniCS (advanced research only)

**build_guide.md** (15 min read)
- Weeks 1–2: Mechanical assembly (wings, body, actuators)
- Weeks 3–4: Electronics (motor driver, wireless module)
- Weeks 5–6: Static thrust test (load cell, function generator)
- Weeks 7–8: Tethered flight test (iPhone slow-mo camera, IMU data)
- Weeks 9–10: Free flight + iteration

### Run All Simulation Modules

```bash
python 00_insect_biomechanics/sim.py    # Wing kinematics + muscle dynamics
python 01_actuator_design/sim.py         # PZT actuator selection
python 02_wing_aerodynamics/sim.py       # MOST IMPORTANT — thrust/frequency
python 06_flight_dynamics/sim.py         # Control loop stability (Bode plots)
python evaluate_all.py                   # Overall status report
```

**Outputs to check**:
- `00_insect_biomechanics/biomechanics.png` — wing beat frequency realistic?
- `02_wing_aerodynamics/thrust_vs_frequency.png` — thrust/weight > 1.5?
- `06_flight_dynamics/bode_and_step.png` — phase margin > 30°?

### Decision: Continue or Redesign?

**All parameters in spec?** → Proceed to Phase 1 (build_guide.md)  
**Something off?** → Stay in Phase 0, adjust simulation, try again

---

## Month 1 — Phase 1 Prototype (Optional)

**IF simulation looks good** (T/W > 1.5, bandwidth > 20 Hz, power < 100 mW):

Follow `build_guide.md` weeks 1–10:

1. **Weeks 1–2**: Order laser-cut wings, 3D print body, source PZT actuators
2. **Weeks 3–4**: Wire up electronics (tethered first, no wireless)
3. **Weeks 5–6**: Static thrust test with load cell (compare to sim)
4. **Weeks 7–8**: Tethered flight in indoor space
5. **Weeks 9–10**: Free flight + iteration

**Cost**: $500–1,500  
**Timeline**: 8–12 weeks  
**Outcome**: Flying robot (validate/refute Phase 0 simulation)

---

## Key Technical Concepts

### 1. Reynolds Number (Re = 500 for you)
- Standard airfoil theory assumes Re > 10,000
- At Re = 500, **leading-edge vortex (LEV) dominates**, not attached flow
- **Solution**: Use unsteady models (Dickinson, Whitney & Wood) or CFD

### 2. Thrust-to-Weight Ratio
- **Minimum**: 1.0 (hovering)
- **Design target**: 1.5–2.0 (margin for control + maneuvers)
- **Check in Module 02 output**

### 3. Control Bandwidth
- **Need**: > 20 Hz (for stable hovering)
- **Limited by**: Actuator speed, wing resonance, sensor latency
- **Verify in Module 06 Bode plot** (phase margin > 30°)

### 4. Power Budget
- **Actuators**: 20–30 mW (dominant cost)
- **Electronics**: 5–10 mW
- **Total**: < 100 mW for practical flight time
- **Battery**: 50 mAh Li-poly = ~10 min flight

### 5. Simulation Is Wrong By ~50%
- This is **expected and normal**
- Phase 0 teaches you the problem
- Phase 1 hardware teaches you the solution
- Expect 3–5 design iterations

---

## Documents to Read (In Order)

| Document | Time | Why |
|---|---|---|
| **This file (START_HERE.md)** | 5 min | Get oriented |
| **plan/ROADMAP.md** | 15 min | Understand the full pipeline |
| **plan/tools_guide.md** | 5 min | Know what to install |
| **plan/build_guide.md** | 20 min | See Phase 1 step-by-step |
| **README.md** | 10 min | Project structure & philosophy |
| **QUICKSTART.md** | 5 min | One-page setup guide |

**Total**: ~60 minutes to fully understand the project

---

## Software You'll Use

| Software | Purpose | Cost | Install Time |
|---|---|---|---|
| Python 3.9+ | Core simulations | Free | 5 min |
| NumPy / SciPy / Matplotlib | Scientific computing & plots | Free | 3 min |
| python-control | Bode plots, transfer functions | Free | 2 min |
| OpenFOAM (optional Tier 2) | CFD validation | Free | 30 min |
| XFOIL (optional Tier 2) | Airfoil analysis | Free | 10 min |
| Elmer FEM (optional Tier 3) | Structural analysis | Free | 15 min |
| MuJoCo (optional Tier 3) | Dynamics simulation | Free | 5 min |

**All free and open-source**

---

## Decision Tree

```
Want to understand the problem?
├─ YES → Read ROADMAP.md + run Module 02 sim
└─ NO → Skip to Phase 1 build_guide.md

Did simulation give T/W > 1.5?
├─ YES → Good! Proceed to Phase 1 build
├─ NO → Redesign in Phase 0 (try different wing size/frequency)
└─ UNSURE → Run OpenFOAM validation (Tier 2, optional)

Ready to build hardware?
├─ YES → Follow build_guide.md weeks 1–4 (order parts)
├─ NO → Stay in simulation, iterate design
└─ LATER → Save all outputs, return when ready
```

---

## Critical Files to Understand

**Simulation Code**:
- `00_insect_biomechanics/sim.py` — Fruit fly kinematics
- `02_wing_aerodynamics/sim.py` — **MOST IMPORTANT** aerodynamic thrust prediction
- `06_flight_dynamics/sim.py` — Control loop design with stability analysis

**Build Instructions**:
- `plan/build_guide.md` — Step-by-step Phase 1 (weeks 1–10)

**Professional Reference**:
- `plan/ROADMAP.md` — Full pipeline documentation
- `plan/tools_guide.md` — Software stack explained

---

## What Happens Next (After You Read)

**Option 1: Pure Simulation Route** (1–2 months)
1. Run all Phase 0 modules
2. Validate against literature (Dickinson, Whitney & Wood)
3. Refine design iteratively
4. Generate design spec for foundry
5. Send to MEMS fabrication (Phase 2)

**Option 2: Build Prototype First** (4–5 months)
1. Run Phase 0 sim (2–4 weeks)
2. Build Phase 1 tethered robot (8–12 weeks)
3. Test and iterate
4. Update simulation with real-world data
5. Then proceed to MEMS (Phase 2)

**Option 3: Learn Incrementally** (flexible)
1. Read ROADMAP.md
2. Run Module 02 (wing aero)
3. Pause, let it sink in
4. Run Module 06 (control)
5. Decide if you want to build

---

## Success Metrics

**After Phase 0 (Simulation)**:
- [ ] All modules run without errors
- [ ] Thrust/weight ratio ≥ 1.5
- [ ] Control bandwidth ≥ 20 Hz
- [ ] Power budget ≤ 100 mW
- [ ] Results match published benchmarks (±20%)

**After Phase 1 (Prototype)**:
- [ ] Static thrust test matches simulation (±30%)
- [ ] Tethered hovering flight > 5 seconds
- [ ] Attitude control responsive to input
- [ ] Flight time > 5 minutes on battery
- [ ] Understand where simulation was wrong

**After Phase 2 (MEMS)**:
- [ ] Autonomous free flight indoors
- [ ] Swarm coordination (multiple robots)
- [ ] Research publications on novel design

---

## Getting Help

**Stuck on simulation?**
- Check `02_wing_aerodynamics/sim.py` output
- Compare to Whitney & Wood (2010) published numbers
- Re-read ROADMAP.md section "Why Insect-Scale Aero Is Different"

**Want to build but not sure where to start?**
- Read `plan/build_guide.md` weeks 1–2
- Order components (parallel with reading)
- Start assembly

**Software issues?**
- See `plan/tools_guide.md` troubleshooting section
- Google the error + "python-control" or "numpy"

---

## One More Thing

> "Simulation is wrong. Hardware is right. Learn from both."
> 
> — MIT RoboBees team (Dario Floreano et al.)

Your first Phase 0 simulation will be wrong by ~50%. This is normal. The point is not accuracy on day 1, but learning the system well enough to build Phase 1. And Phase 1 will teach you more than any simulation ever could.

---

## Next Action (Right Now)

```bash
# 1. Read this file (you're done!)

# 2. Read ROADMAP.md
open plan/ROADMAP.md

# 3. Install software
pip install numpy scipy matplotlib python-control

# 4. Run the wing aerodynamics module
python 02_wing_aerodynamics/sim.py

# 5. Look at the plot
open 02_wing_aerodynamics/thrust_vs_frequency.png

# 6. Ask: Is thrust/weight > 1.5?
#    If yes  → read build_guide.md
#    If no   → stay in Phase 0, redesign
```

---

**You're ready. Go build something amazing! 🚁**
