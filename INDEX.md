# Complete Professional Pipeline — File Index

Everything you need to design, simulate, build, and fabricate flapping-wing microrobots.

---

## Getting Started (Read These First)

| File | Length | Purpose | Next |
|---|---|---|---|
| **START_HERE.md** | 10 min | Orientation & what you have | → ROADMAP.md |
| **CHECKLIST.md** | 5 min | Track your progress | → phase-specific docs |
| **QUICKSTART.md** | 3 min | Install & run in 5 min | → Module 02 |

---

## Professional Guides (plan/ directory)

| File | Length | Audience | Key Sections |
|---|---|---|---|
| **plan/ROADMAP.md** | 30 min | Everyone | Phase 0/1/2 overview, Reynolds number, 3 sim paths, timeline & budget |
| **plan/tools_guide.md** | 15 min | Coders | Install tiers (Python/OpenFOAM/MuJoCo), decision tree |
| **plan/build_guide.md** | 25 min | Builders | Phase 1 weeks 1–10, BOM, troubleshooting |
| **plan/SUMMARY.md** | 10 min | Decision makers | Executive summary, key insights, next steps |

**Reading Order**:
1. START_HERE.md (understand what you have)
2. plan/ROADMAP.md (full context)
3. Choose your path:
   - Simulation only? → plan/tools_guide.md
   - Want to build? → plan/build_guide.md
4. plan/SUMMARY.md (quick reference)

---

## Simulation Modules (Upgraded with Real Physics)

### Critical Module (Most Important)

| Module | File | Physics Model | Status |
|---|---|---|---|
| **02 — Wing Aerodynamics** | `02_wing_aerodynamics/sim.py` | Whitney & Wood quasi-static flapping + Dickinson LEV correction | ✅ **Professional** |
| | `02_wing_aerodynamics/evaluator.py` | Grading against thrust benchmarks | ✅ Working |
| | `02_wing_aerodynamics/results.md` | Output: thrust vs. frequency, T/W ratio, power | Auto-filled by sim |

**Why This Module**: Predicts if you can hover (thrust/weight ratio > 1.0)

---

### Foundation Modules

| Module | File | What | Status |
|---|---|---|---|
| **00 — Biomechanics** | `00_insect_biomechanics/sim.py` | Fruit fly kinematics, muscle dynamics, wing frequency | ✅ Enhanced |
| | Includes: | Dickinson unsteady corrections, control bandwidth analysis | |
| | Output: | Wing beat frequency, muscle force, CoG location | |
| **01 — Actuators** | `01_actuator_design/sim.py` | PZT bimorph selection, force-frequency curves | ⏳ Pending |
| | Output: | Actuator type, resonance, power consumption | |
| **06 — Flight Dynamics** | `06_flight_dynamics/sim.py` | PID control, 6-DOF attitude dynamics, Bode plots | ✅ Enhanced |
| | Output: | Phase margin, gain margin, stability analysis | |

**Run Order**: 00 → 02 → 06 (each builds on previous)

---

### Support Modules (Required for Full Analysis)

| Module | Purpose |
|---|---|
| **03 — Power Management** | Battery budget, flight endurance |
| **04 — Control Electronics** | Wireless, MCU, latency analysis |
| **05 — Structural Design** | Wing resonance, stress analysis |
| **07 — Swarm Coordination** | Multi-robot communication |
| **08 — Fabrication Plan** | MEMS process flow, foundry options |
| **09 — Full-Chain Integration** | Final go/no-go assessment |

---

## How to Run Simulations

### Quick Start (2 minutes)

```bash
cd robotic-insects/
python 02_wing_aerodynamics/sim.py
```

Check: Is thrust-to-weight ratio > 1.5? (If yes, you can hover)

### Full Suite (5 minutes)

```bash
python 00_insect_biomechanics/sim.py
python 01_actuator_design/sim.py
python 02_wing_aerodynamics/sim.py
python 06_flight_dynamics/sim.py
python evaluate_all.py
```

Output: All plots + final status report

---

## Phase-Specific Documentation

### Phase 0: Simulation Only

**Duration**: 1–4 weeks (depending on validation)  
**Cost**: $0  
**Outcome**: Design spec (T/W ratio, power, control stability)

**Files to Read**:
- plan/ROADMAP.md (Phase 0 section)
- plan/tools_guide.md (Tier 1 Python + optional Tier 2 CFD)

**Key Modules to Run**:
- 02_wing_aerodynamics/sim.py (most important)
- 06_flight_dynamics/sim.py (control stability)

**Success Criteria**:
- [ ] T/W ratio > 1.5
- [ ] Control bandwidth > 20 Hz
- [ ] Power < 100 mW
- [ ] All evaluators PASS

---

### Phase 1: Bench Prototype

**Duration**: 8–12 weeks  
**Cost**: $500–1,500  
**Outcome**: Flying robot (5+ sec hover), validation of sim

**Files to Read**:
- plan/build_guide.md (complete step-by-step)
- plan/ROADMAP.md (Phase 1 section)

**Timeline**:
- Weeks 1–2: Mechanical (wings, body, actuators)
- Weeks 3–4: Electronics (motor driver, wireless)
- Weeks 5–6: Static thrust test (load cell)
- Weeks 7–8: Tethered dynamic flight
- Weeks 9–10: Free flight + iteration

**BOM Highlights**:
- PZT bimorph actuators: $200–400
- 3D printed body: $100
- Laser-cut wings: $100
- Electronics PCB: $50–100
- Battery: $15

**Success Criteria**:
- [ ] Robot hovers free for > 5 sec
- [ ] Thrust matches sim (±30%)
- [ ] Battery lasts > 5 min

---

### Phase 2: MEMS Fabrication

**Duration**: 20 weeks  
**Cost**: $100k+  
**Outcome**: Integrated MEMS chip with built-in actuators

**Files to Reference**:
- design/spec_sheet.md (performance targets)
- design/fabrication_traveler.md (foundry instructions)
- design/bom.md (MEMS components)
- design/test_protocol.md (validation plan)
- design/mems_layout/*.py (GDS-II generation)

**Foundry Options**:
- Sandia SUMMIT V (USA, 16 weeks, $50–100k)
- SiTime MEMS+ (international, 12 weeks, $50–200k)
- MIT.nano / Stanford SNF (academic, 8 weeks, $1–2k labor)
- Commercial (China, 12 weeks, $20–80k)

---

## Key Technical References (Implemented in Code)

| Author | Year | Paper | Module | How Used |
|---|---|---|---|---|
| Dickinson et al. | 2000 | Unsteady aerodynamics in Drosophila | 00, 02 | LEV lift correction (+30%) |
| Whitney & Wood | 2010 | Quasi-static flapping model | 02 | Core aerodynamic equations |
| Combes & Dudley | 2002 | Stability limits at Re=100–1000 | 06 | Bandwidth requirement |
| Beard & McLain | 2012 | Small aircraft control theory | 06 | PID design, Bode analysis |
| Tanaka et al. | 2013 | Piezo actuator scaling | 01 | Force-frequency curves |

---

## File Organization

```
robotic-insects/
│
├── START_HERE.md               ← Read this first (30 min)
├── INDEX.md                    ← This file (navigation)
├── CHECKLIST.md                ← Track your progress
├── QUICKSTART.md               ← 5-min setup
├── README.md                   ← Project overview & philosophy
│
├── plan/                       ← PROFESSIONAL GUIDES (read in order)
│   ├── ROADMAP.md             ← Full pipeline (30 min)
│   ├── tools_guide.md         ← Software installation (15 min)
│   ├── build_guide.md         ← Phase 1 build (25 min)
│   └── SUMMARY.md             ← Executive summary (10 min)
│
├── evaluate_all.py             ← Master evaluator (run anytime)
│
├── 00_insect_biomechanics/     ← WAVE 1: Foundations
│   ├── requirements.md
│   ├── sim.py                 ← ✅ Enhanced: Dickinson model
│   ├── evaluator.py
│   └── results.md
│
├── 01_actuator_design/         ← WAVE 1: Actuators
│   ├── requirements.md
│   ├── sim.py                 ← Piezo selection
│   ├── evaluator.py
│   └── results.md
│
├── 02_wing_aerodynamics/       ← WAVE 2: MOST IMPORTANT
│   ├── requirements.md
│   ├── sim.py                 ← ✅ **PROFESSIONAL**: Whitney & Wood model
│   ├── evaluator.py
│   ├── results.md
│   └── thrust_vs_frequency.png ← Output plot
│
├── 03_power_management/        ← WAVE 2: Power budget
├── 04_control_electronics/     ← WAVE 2: MCU & wireless
├── 05_structural_design/       ← WAVE 2: FEM resonance
│
├── 06_flight_dynamics/         ← WAVE 3: Control
│   ├── requirements.md
│   ├── sim.py                 ← ✅ Enhanced: 6-DOF, Bode plots
│   ├── evaluator.py
│   ├── results.md
│   └── bode_and_step.png      ← Output plot
│
├── 07_swarm_coordination/      ← WAVE 3: Multi-robot
├── 08_fabrication_plan/        ← WAVE 4: MEMS foundry
├── 09_fullchain/               ← WAVE 4: Final integration
│
└── design/                     ← PHASE 2 OUTPUTS
    ├── spec_sheet.md
    ├── fabrication_traveler.md
    ├── bom.md
    ├── test_protocol.md
    └── mems_layout/
        ├── wing_pattern_v1.py  (GDS-II generator)
        ├── actuator_array_v1.py
        └── body_profile_v1.py
```

---

## Recommended Reading Path

### Path 1: Quick Learner (1 hour)
1. START_HERE.md (10 min)
2. plan/ROADMAP.md "Phase 0" section (15 min)
3. Run `python 02_wing_aerodynamics/sim.py` (2 min)
4. Look at `thrust_vs_frequency.png` (2 min)
5. Decide: continue Phase 0 or go to Phase 1?

### Path 2: Full Understanding (2 hours)
1. START_HERE.md (10 min)
2. plan/ROADMAP.md (full, 30 min)
3. plan/tools_guide.md (15 min)
4. plan/build_guide.md (20 min)
5. Run all simulations (10 min)
6. plan/SUMMARY.md (10 min)

### Path 3: Builder's Path (1.5 hours)
1. START_HERE.md (10 min)
2. plan/ROADMAP.md "Phase 1" section (10 min)
3. plan/build_guide.md (30 min)
4. CHECKLIST.md Phase 1 section (5 min)
5. Decide: order components now or sim first?

---

## Quick Decision Tree

```
New to this project?
├─ YES → Read START_HERE.md first
└─ NO  → Proceed

Want to just run the sim?
├─ YES → pip install + python 02_wing_aerodynamics/sim.py
└─ NO  → Read plan/ROADMAP.md

Want to build hardware?
├─ YES → Read plan/build_guide.md + CHECKLIST.md
└─ NO  → Stay in Phase 0 simulation

Need validation (CFD)?
├─ YES → Read plan/tools_guide.md Tier 2
└─ NO  → Use Phase 0 results as-is

Ready for foundry (MEMS)?
├─ YES → Use design/ files, submit to MEMS foundry
└─ NO  → Complete Phase 1 build first
```

---

## Key Outputs You'll Generate

| Phase | Output | Used For |
|---|---|---|
| **Phase 0** | thrust_vs_frequency.png | Check if T/W > 1.5 (can hover) |
| **Phase 0** | bode_and_step.png | Verify control stability (margins > spec) |
| **Phase 0** | spec_sheet.md | Foundry spec (Phase 2) or investor pitch |
| **Phase 1** | Flight video | Validation proof, paper publication |
| **Phase 1** | Load cell data | Compare hardware vs. simulation |
| **Phase 2** | *.gds (GDS-II files) | Send to MEMS foundry for fabrication |

---

## Troubleshooting Guide

### Simulation Won't Run

**Problem**: `ModuleNotFoundError: No module named 'numpy'`
- **Solution**: `pip install numpy scipy matplotlib python-control`

**Problem**: `AttributeError: module 'numpy' has no attribute 'trapz'`
- **Solution**: Use `from numpy import trapz` at top of file

**Problem**: Python script runs but no plot appears
- **Solution**: Plots are saved to files, check the `.png` output files

### Phase 1 Build Issues

**Problem**: Wings not moving
- **Solution**: Check epoxy bond (gently tug wing), verify electrical connections

**Problem**: Thrust is 50% lower than simulation
- **Solution**: Increase voltage (30V max), stiffer wings, or larger actuators (expected on first build)

**Problem**: Robot not stable in flight
- **Solution**: Adjust PID gains (reduce proportional term), check wing symmetry

---

## Contact & Help

- **Simulation questions**: Compare outputs to Whitney & Wood (2010) published numbers
- **Build questions**: Check troubleshooting in plan/build_guide.md
- **MEMS questions**: Contact your chosen foundry (Sandia, SiTime, Stanford, etc.)

---

## Next Step

```bash
# Right now (next 5 minutes):
pip install numpy scipy matplotlib python-control
python robotic-insects/02_wing_aerodynamics/sim.py
open robotic-insects/02_wing_aerodynamics/thrust_vs_frequency.png

# Ask yourself: Is thrust-to-weight ratio > 1.5?
# If YES → Continue to Phase 1
# If NO  → Adjust simulation parameters, try again
```

**Good luck!** 🚁

---

**Last Updated**: 2026-04-03  
**Status**: Complete Phase 0 scaffold + upgraded simulation modules + professional guides for Phase 1 & 2
