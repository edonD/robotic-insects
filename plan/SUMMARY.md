# Professional Pipeline Summary: Simulation → Build

**Document Type**: Executive summary & quick reference  
**Created**: 2026-04-03  
**Target**: Flapping-wing microrobot (5–50 mg, aerial)

---

## Three Critical Documents

You now have three professional guides in `robotic-insects/plan/`:

### 1. **ROADMAP.md** ⭐ Read This First
**What**: Full pathway from simulation → Phase 1 build → Phase 2 MEMS  
**Coverage**:
- Why insect-scale aerodynamics is special (Re = 100–1000, leading-edge vortex dominates)
- Three simulation paths (Fast Python / Medium validated / Slow detailed co-sim)
- Phase 1 build timeline, budget, and what will go wrong
- Phase 2 MEMS fabrication (foundries, costs, timeline)
- Key papers to implement in simulation

**Key Insight**: Simulation is wrong by ~50% first time. Phase 1 build teaches you the reality.

---

### 2. **tools_guide.md** ⭐ Install These
**What**: Software installation guide for 4 tiers

**Tier 1** (Right now, free): Python + NumPy/SciPy/Matplotlib
- 5 min install
- Ready to run Wing Aerodynamics sim

**Tier 2** (If needed): OpenFOAM + XFOIL for CFD validation
- 45 min install
- Validate 1–2 wing designs with Navier-Stokes

**Tier 3** (Advanced): Elmer FEM + MuJoCo for full coupling
- 1.5 hr install
- Research-grade co-simulation

**Tier 4** (Optional): FEniCS for custom FSI
- Very high learning curve
- Only if doing novel research

**Recommendation**: Install Tier 1 today, add Tier 2 after Phase 0 sim is working.

---

### 3. **build_guide.md** ⭐ Phase 1 Prototype
**What**: Step-by-step build instructions for tethered robot (8–12 weeks, $500–1500)

**Week 1–2**: Mechanical assembly
- Laser-cut carbon fiber wings (3–4 mm span)
- 3D print thorax (2–3 mg)
- Glue off-the-shelf PZT bimorph actuators

**Week 3–4**: Electronics
- Choose: tethered only (cheaper, simpler) OR wireless (BLE module)
- Motor driver, power amplifier, oscillator

**Week 5–6**: Static thrust test
- Measure thrust vs. frequency with load cell
- Compare to simulation predictions (will likely be off by 50%)

**Week 7–8**: Tethered dynamic flight
- Hang from monofilament in indoor space
- Slow-mo video (iPhone 240 fps)
- Verify wing frequency and control authority

**Week 9–10**: Free flight iteration
- Remove tether gradually
- Tune control gains based on actual behavior

**Key Component Costs**:
- PZT actuators: $200–400 (most expensive)
- 3D printed body: $100
- Carbon wings: $100
- Electronics PCB: $50–100
- Battery: $15

---

## Simulation Module Upgrades

You have 4 critical modules to run:

| Module | What | Improvement | Status |
|---|---|---|---|
| **00** — Biomechanics | Fruit fly kinematics, muscle dynamics | Added Dickinson unsteady corrections | ✓ Enhanced |
| **02** — Wing Aero | **MOST IMPORTANT** | Implemented Whitney & Wood quasi-static model + Bode plots | ✓ Professional |
| **06** — Flight Dynamics | Attitude control loop design | Added 6-DOF dynamics, phase/gain margin analysis | ✓ Enhanced |
| **01** — Actuators | Piezo selection & scaling | Updated with real PZT bimorph curves | Pending |

---

## How to Use This Pipeline

### **Right Now (Today)**

```bash
# Step 1: Install Tier 1
pip install numpy scipy matplotlib python-control

# Step 2: Run the aerodynamics module
cd robotic-insects/
python 02_wing_aerodynamics/sim.py

# You'll see:
# - Thrust vs. frequency curve
# - Thrust/weight ratio
# - Power budget
# - Plot saved to: thrust_vs_frequency.png

# Step 3: Compare to literature
# Check the output:
# - Is thrust/weight > 1.5? (you need margin for control)
# - Is thrust at 200 Hz reasonable for your wing design?
# - Does power < 100 mW? (battery feasible)
```

### **This Week**

```bash
# Step 1: Read ROADMAP.md fully
# (1 hour)

# Step 2: Run all simulation modules
python 00_insect_biomechanics/sim.py
python 01_actuator_design/sim.py
python 02_wing_aerodynamics/sim.py
python 06_flight_dynamics/sim.py
python evaluate_all.py

# Step 3: Look at plots
# - biomechanics.png: is wing kinematics realistic?
# - thrust_vs_frequency.png: can you hover?
# - bode_and_step.png: is control stable?

# Step 4: Identify critical unknowns
# - Does simulation match literature? (Dickinson, Whitney & Wood, Combes & Dudley)
# - If not, what's wrong? (wrong Reynolds number? bad assumptions?)
```

### **Month 1: Validate Simulation**

Option A: **Run CFD validation** (if sim seems off)
```bash
# Install OpenFOAM (Tier 2, ~45 min)
# Run 1–2 wing conditions in CFD
# Compare to Whitney & Wood output
# If CFD > 20% different from sim: refine model
```

Option B: **Build Phase 1 prototype** (if sim looks good)
```bash
# Order laser-cut wings, 3D print body, source PZT actuators
# Follow build_guide.md weeks 1–4
# Static thrust test: does hardware match sim?
# (Usually off by 50% first time — debug this)
```

### **Month 3–5: Phase 1 Build**

- Weeks 1–4: mechanical + electrical assembly
- Weeks 5–6: static thrust characterization
- Weeks 7–8: tethered dynamic flight test
- Weeks 9–10: free flight + iteration

**Success criterion**: Robot hovers stable for > 5 seconds

### **Month 6–8: Design Refinement**

- Compare Phase 1 results to Phase 0 simulation
- Update simulation with real-world insights
- Run CFD validation on final wing design
- Prepare specification for MEMS foundry

### **Month 9–14: Phase 2 MEMS Fabrication**

- Send GDS-II layouts to foundry
- 8–20 week fabrication + testing
- Integrate MEMS body with off-the-shelf electronics
- First MEMS prototype flight

---

## What You're Implementing (Literature)

| Paper | Key Contribution | How to Use |
|---|---|---|
| **Dickinson et al. (2000)** | Unsteady forces (LEV, rotational lift) | Module 00: adds ~30% to quasi-steady thrust |
| **Whitney & Wood (2010)** | Quasi-static flapping model | Module 02: core aerodynamic predictions |
| **Combes & Dudley (2002)** | Stability limits at Re=100–1000 | Module 06: control bandwidth requirement |
| **Tanaka et al. (2013)** | PZT actuator scaling | Module 01: force-frequency curves |
| **Beard & McLain (2012)** | Control theory for small aircraft | Module 06: PID design, Bode analysis |

---

## Key Technical Insights

### 1. Reynolds Number Matters
- **You**: Re ≈ 500 (fruit fly scale)
- **Standard airfoil theory**: Re > 10,000 (doesn't apply!)
- **Consequence**: Leading-edge vortex (LEV) is your primary lift source
- **Solution**: Use unsteady force models or CFD, not thin-airfoil theory

### 2. Thrust-to-Weight Ratio
- **Minimum**: 1.0 (hovering)
- **Design target**: 1.5–2.0 (margin for control + maneuvering)
- **If < 1.0**: Simulation was optimistic, redesign needed

### 3. Control Bandwidth
- **Needed**: > 20 Hz (for stable hovering)
- **Limited by**: Actuator response time + structural resonance + electronics latency
- **Check with**: Bode plots (phase margin > 30°, gain margin > 6 dB)

### 4. Power Budget
- **Actuators**: 20–30 mW (dominant)
- **Electronics**: 5–10 mW
- **Total**: < 100 mW for practical flight time
- **Battery**: 50 mAh Li-poly gives ~10 min flight at 100 mW

### 5. First Prototype Will Be Wrong
- Phase 0 simulation: ±50% error (normal!)
- Phase 1 build reveals: wing flexibility, epoxy joint stiffness, actuator efficiency losses
- Iteration: expect 3–5 design cycles before flying well
- **This is intentional**: simulation teaches you the problem, hardware teaches you the solution

---

## Decision Tree: Which Path?

```
Do you have 1–2 hours to explore simulation?
  ├─ YES → Run Path A (sim only)
  │         python 02_wing_aerodynamics/sim.py
  │         (see if thrust/weight > 1.5)
  │
  └─ NO → Read ROADMAP.md (1 page/minute)
          Get intuition for the problem
          Then come back and run simulation

Is simulation result T/W > 1.5?
  ├─ YES → Go to Phase 1 build (build_guide.md)
  │         Order components, start fabrication
  │
  └─ NO → Stay in Phase 0, redesign
          Change wing size, frequency, stroke amplitude
          Try again

Is Phase 1 prototype hovering stably?
  ├─ YES → Design is validated
  │         Can proceed to Phase 2 (MEMS)
  │
  └─ NO → Debug (most likely: wing stiffness or actuator)
          Update Phase 0 sim with real-world data
          Iterate design
```

---

## Next Action Items

- [ ] Read `ROADMAP.md` (start to finish, 1 hour)
- [ ] Read `tools_guide.md` (skim, 10 minutes)
- [ ] Run: `python 02_wing_aerodynamics/sim.py`
- [ ] Check: `02_wing_aerodynamics/thrust_vs_frequency.png`
- [ ] Decide: Does thrust/weight look feasible? (> 1.5)
- [ ] If yes: read `build_guide.md` and start Phase 1
- [ ] If no: adjust simulation, try again

---

## Bottom Line

**3-phrase summary**:

1. **Phase 0 (Simulation)**: 8 weeks, $5k in compute time, predicts ±50% of reality
2. **Phase 1 (Bench Prototype)**: 12 weeks, $1.5k, validates what simulation got wrong
3. **Phase 2 (MEMS)**: 20 weeks, $100k+, produces manufacturable design

**Your job now**: Complete Phase 0 (run simulations), read the guides, then decide if Phase 1 is worth building.

Good luck! 🚁

---

## Files Structure

```
robotic-insects/
├── plan/
│   ├── ROADMAP.md          ← Professional pipeline (full, 2000 lines)
│   ├── tools_guide.md      ← Software installation (1000 lines)
│   ├── build_guide.md      ← Phase 1 build (3000 lines, step-by-step)
│   └── SUMMARY.md          ← This file (quick reference)
├── QUICKSTART.md           ← 5-min setup
├── README.md               ← Project overview
├── evaluate_all.py         ← Master evaluator
├── 00_insect_biomechanics/ ← ✓ Enhanced with Dickinson model
├── 01_actuator_design/     ← Pending upgrade
├── 02_wing_aerodynamics/   ← ✓ Whitney & Wood quasi-static model (PROFESSIONAL)
├── 06_flight_dynamics/     ← ✓ 6-DOF dynamics + Bode plots
└── [other modules...]
```

---

**Start here**: Open `ROADMAP.md` and read the "Phase 0: Simulation" section.
