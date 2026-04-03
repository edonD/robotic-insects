# ROBOTIC INSECTS — Micro-Aerial & Legged Robots
## Insect-Inspired MEMS Actuators | Agile Flight & Locomotion | Autonomous Microrobots

---

## What This Is

A comprehensive design framework for building biomimetic microrobots based on insect mechanics:
- **Aerial robots**: Flapping-wing flight inspired by fruit flies & bees (50–200 Hz wing beats)
- **Legged robots**: Hexapod/quadrupod locomotion using shape-memory alloy or piezo actuators
- **Hybrid systems**: Bio-inspired control algorithms for swarm coordination

**Target specifications:**
- Robot mass           : 5–50 mg
- Flight duration      : 5–30 minutes (wireless power or optimized batteries)
- Wing beat frequency  : 100–200 Hz
- Speed                : 2–5 m/s
- Maneuverability      : 10+ consecutive flips, hovering stability
- Applications        : Pollination, disaster search & rescue, environmental monitoring

---

## The Evaluator Is the Design

Every module contains an `evaluator.py`. This grades simulation results against:
- Published biomechanics literature (insect kinematics, aerodynamics)
- State-of-the-art robot prototypes (MIT RoboBees, Harvard Wyss microrobots)
- Fabrication constraints (MEMS scalability, materials available)

**Grading system:**
```
PASS      — within target, feasible with current fab methods
MARGINAL  — within target but requires advanced techniques, flag for review
FAIL      — outside target, redesign required, do not proceed
```

Run the master evaluator at any time:
```
python evaluate_all.py
```

---

## Folder Structure

```
robotic-insects/
│
├── README.md                        ← this file
├── evaluate_all.py                  ← master evaluator: runs all waves
│
├── requirements/                    ← SOFTWARE INSTALLATION
│   ├── README.md                    ← what to install and why
│   ├── 01_python.md                 ← numpy, scipy, matplotlib, control, CFD tools
│   ├── 02_ansys_cfd.md              ← ANSYS Fluent or OpenFOAM (aerodynamics)
│   ├── 03_fem_structures.md         ← Elmer FEM for structural analysis
│   └── 04_gdstk_layout.md           ← gdstk for MEMS layout (wing patterns, actuator arrays)
│
├── ── WAVE 1 ── (Foundations, run in parallel) ──────────────────────────────
│
├── 00_insect_biomechanics/          ← [WAVE 1] BIOLOGICAL REFERENCE
│   ├── requirements.md              ← questions to answer from literature
│   ├── sim.py                       ← kinematic model: wing motion, muscle activation
│   ├── evaluator.py                 ← grades against Drosophila & bee data
│   └── results.md                   ← extracted biomechanics (filled after sim)
│
├── 01_actuator_design/              ← [WAVE 1] ARTIFICIAL MUSCLES
│   ├── requirements.md
│   ├── sim.py                       ← piezo/SMA performance model
│   ├── evaluator.py                 ← grades force, frequency, power, scaling
│   └── results.md
│
├── ── WAVE 2 ── (Subsystems, after Wave 1) ──────────────────────────────────
│
├── 02_wing_aerodynamics/            ← [WAVE 2] needs: 00
│   ├── requirements.md
│   ├── sim.py                       ← CFD/analytical (lift, drag, torque per wingbeat)
│   ├── evaluator.py                 ← grades thrust, efficiency, control margins
│   └── results.md
│
├── 03_power_management/             ← [WAVE 2] needs: 01 + 02
│   ├── requirements.md
│   ├── sim.py                       ← energy budget: power draw, battery/harvesting options
│   ├── evaluator.py                 ← grades flight time, weight penalty, feasibility
│   └── results.md
│
├── 04_control_electronics/          ← [WAVE 2] needs: 01
│   ├── requirements.md
│   ├── sim.py                       ← wireless receiver, micro-controller (ARM Cortex-M0), driver power
│   ├── evaluator.py                 ← grades size, weight, latency, frequency response
│   └── results.md
│
├── 05_structural_design/            ← [WAVE 2] needs: 00 + 01
│   ├── requirements.md
│   ├── sim.sif                      ← Elmer FEM: thorax stiffness, stress distribution
│   ├── geometry.FCStd               ← FreeCAD model: body, exoskeleton
│   ├── evaluator.py                 ← grades resonance avoidance, deflection, weight
│   └── results.md
│
├── ── WAVE 3 ── (Integration & Control, after Wave 2) ──────────────────────
│
├── 06_flight_dynamics/              ← [WAVE 3] needs: 00 + 02 + 04
│   ├── requirements.md
│   ├── sim.py                       ← attitude dynamics, PID flight controller
│   ├── evaluator.py                 ← grades stability, response time, maneuver capability
│   └── results.md
│
├── 07_swarm_coordination/           ← [WAVE 3] needs: 04 + 06
│   ├── requirements.md
│   ├── sim.py                       ← acoustic/RF swarm model, emergent behavior
│   ├── evaluator.py                 ← grades scalability, coordination reliability
│   └── results.md
│
├── ── WAVE 4 ── (Manufacturing & Validation, after Wave 3) ────────────────
│
├── 08_fabrication_plan/             ← [WAVE 4] needs: 01 + 05
│   ├── requirements.md
│   ├── process_flow.md              ← step-by-step MEMS/assembly instructions
│   ├── evaluator.py                 ← grades process maturity, yield, cost
│   └── results.md
│
├── 09_fullchain/                    ← [WAVE 4] needs: everything
│   ├── requirements.md
│   ├── sim.py                       ← end-to-end integrated model
│   ├── evaluator.py                 ← final go/no-go: all specs met?
│   └── results.md
│
├── ── PHASE 2: DESIGN OUTPUTS ───────────────────────────────────────────────
│
└── design/                          ← compiled from all results
    ├── spec_sheet.md                ← performance spec (mass, flight time, speed, etc.)
    ├── fabrication_traveler.md      ← fab instructions (MEMS foundry, assembly)
    ├── bom.md                       ← bill of materials
    ├── test_protocol.md             ← wind tunnel, flight testing procedures
    └── mems_layout/                 ← mask & actuator array designs
        ├── README.md
        ├── wing_pattern_v1.py       ← gdstk: wing vein pattern
        ├── actuator_array_v1.py     ← gdstk: piezo actuator layout
        └── body_profile_v1.py       ← gdstk: overall body outline
```

---

## Execution Order

```
STEP 1 — Install Software
    → read requirements/README.md
    → follow 01_python.md + 02_ansys_cfd.md + 03_fem_structures.md + 04_gdstk_layout.md

STEP 2 — Wave 1 (parallel, foundation)
    → python 00_insect_biomechanics/sim.py
    → python 01_actuator_design/sim.py
    → run evaluators
    → BOTH must PASS before Wave 2

STEP 3 — Wave 2 (parallel, after Wave 1 passes)
    → python 02_wing_aerodynamics/sim.py
    → python 03_power_management/sim.py
    → python 04_control_electronics/sim.py
    → elmer 05_structural_design/sim.sif
    → run all evaluators
    → ALL must PASS before Wave 3

STEP 4 — Wave 3 (after Wave 2 passes)
    → python 06_flight_dynamics/sim.py
    → python 07_swarm_coordination/sim.py
    → run evaluators

STEP 5 — Wave 4 (after Wave 3 passes)
    → python 08_fabrication_plan/process_flow.md (document review)
    → python 09_fullchain/sim.py
    → python 09_fullchain/evaluator.py
    → PASS here = proceed to Phase 2

STEP 6 — Phase 2: Design Package
    → compile design/spec_sheet.md from all results
    → compile design/fabrication_traveler.md
    → run design/mems_layout/*.py (generates mask patterns)
    → compile design/bom.md
    → write design/test_protocol.md
```

Or run everything:
```
python evaluate_all.py
```

---

## Benchmark References

All evaluators grade against these published sources:

| Source | Module | Used For |
|---|---|---|
| Dickinson et al. (2000) — Drosophila dynamics | 00, 02 | Wing kinematics, aerodynamic coefficients |
| Fry et al. (2005) — Fruit fly control | 06 | Flight dynamics, neural control |
| MIT RoboBees papers (2013–2025) | 01, 04, 06 | Actuator scaling, flight controller design |
| Harvard Wyss Microrobotics (2022–2025) | 03, 07, 08 | Power budgets, swarm algorithms |
| Kiens et al. — Insect muscle mechanics | 00, 01 | Force-velocity relationships, activation |
| ANSYS Fluent / OpenFOAM validation | 02 | Wing aerodynamic database |

---

## Dependencies Between Modules

```
00_insect_biomechanics ──────────────────┐
    └──→ 02_wing_aerodynamics            │
    └──→ 05_structural_design (partial)  │
    └──→ 06_flight_dynamics              │
                                         │
01_actuator_design ──────────────────────┤
    └──→ 03_power_management             │
    └──→ 04_control_electronics          │
    └──→ 05_structural_design            │
    └──→ 06_flight_dynamics (partial)    │
                                         │
02_wing_aerodynamics ────────────────────┤
    └──→ 03_power_management             │
    └──→ 06_flight_dynamics ─────────────┤
                                         │
04_control_electronics ──────────────────┤
    └──→ 06_flight_dynamics ─────────────┤
    └──→ 07_swarm_coordination ──────────┤
                                         │
05_structural_design ────────────────────┤
    └──→ 08_fabrication_plan ────────────┤
                                         │
06_flight_dynamics ──────────────────────┤
    └──→ 07_swarm_coordination ──────────┤
                                         │
07_swarm_coordination ───────────────────┤
    └──→ 09_fullchain ───────────────────┤
                                         │
08_fabrication_plan ─────────────────────┤
    └──→ 09_fullchain ───────────────────┘
```

---

## What Phase 1 Produces (inputs to Phase 2)

| Module | Data Extracted | Goes Into |
|---|---|---|
| 00_insect_biomechanics | Wing beat freq (Hz), muscle activation pattern, CoG location | spec_sheet, 02, 06 |
| 01_actuator_design | Force per actuator (mN), frequency response (Hz), power (mW) | 03, 04, 05, spec_sheet |
| 02_wing_aerodynamics | Thrust/weight ratio, drag coeff, control authority per angle | spec_sheet, 06 |
| 03_power_management | Flight time (min), battery mass (mg), energy density needed | spec_sheet, test_protocol |
| 04_control_electronics | Receiver latency (ms), CPU freq (MHz), wireless range (m) | spec_sheet, 06 |
| 05_structural_design | Body mass (mg), resonance frequency (Hz), max stress (MPa) | mems_layout, fabrication_traveler |
| 06_flight_dynamics | Loop bandwidth (Hz), phase margin (deg), max accel (g) | spec_sheet, test_protocol |
| 07_swarm_coordination | Communication protocol, collision avoidance range (cm) | spec_sheet, bom |
| 08_fabrication_plan | Process steps, materials, yield estimate (%) | fabrication_traveler, bom |
| 09_fullchain | Go/No-Go: full system meets all specs | everything |

---

## Key Challenges This Framework Addresses

1. **Miniaturization Gap**: How small can actuators be while maintaining force & control bandwidth?
2. **Power Budget**: Flight time vs. weight—batteries are heavy at this scale
3. **Resonance Avoidance**: Body structure must not vibrate at wing frequency (100–200 Hz)
4. **Control Stability**: Insect-scale aerodynamics are nonlinear & prone to instability
5. **Manufacturing Tolerance**: MEMS precision needed; yield & cost scaling
6. **Swarm Coordination**: Distributed control with minimal communication overhead

Each module isolates one challenge, evaluates it strictly, then passes results downstream.

---

## Next Steps

1. **Install software**: `cd requirements && follow README.md`
2. **Start Wave 1**: `python 00_insect_biomechanics/sim.py`
3. **Check progress**: `python evaluate_all.py`
