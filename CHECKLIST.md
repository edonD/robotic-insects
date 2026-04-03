# Professional Pipeline Checklist

Use this to track your progress through Phase 0, Phase 1, and Phase 2.

---

## Phase 0: Simulation (Weeks 1–8)

### Week 1: Setup & First Run

- [ ] Read `START_HERE.md` (30 min)
- [ ] Read `plan/ROADMAP.md` section "Phase 0: Simulation" (20 min)
- [ ] Install Python packages: `pip install numpy scipy matplotlib python-control`
- [ ] Verify install: `python -c "import numpy; print('OK')"`
- [ ] Run: `python 02_wing_aerodynamics/sim.py`
- [ ] Check output: `02_wing_aerodynamics/thrust_vs_frequency.png` exists
- [ ] Answer: Is thrust-to-weight ratio > 1.5? (YES/NO/___)

### Week 2: Run All Modules

- [ ] Run: `python 00_insect_biomechanics/sim.py`
  - Wing beat frequency: ___ Hz
  - Muscle force: ___ mN
- [ ] Run: `python 01_actuator_design/sim.py`
  - Actuator type: _______________
  - Force: ___ mN
- [ ] Run: `python 02_wing_aerodynamics/sim.py` (again, save output)
  - Thrust: ___ mN
  - T/W ratio: ___
- [ ] Run: `python 06_flight_dynamics/sim.py`
  - Phase margin: ___ ° (target: > 30°)
  - Gain margin: ___ dB (target: > 6 dB)
- [ ] Run: `python evaluate_all.py` (master evaluator)
  - Wave 1 PASS? (YES/NO)
  - Wave 2 PASS? (YES/NO)

### Week 3–4: Compare to Literature

- [ ] Read Dickinson et al. (2000) section on unsteady forces
  - LEV correction factor: ___
  - Your simulation accounts for this? (YES/NO)

- [ ] Read Whitney & Wood (2010) on quasi-static flapping
  - Benchmark thrust (their Table 2): ___ mN
  - Your simulation thrust: ___ mN
  - Within ±30%? (YES/NO)

- [ ] Read Combes & Dudley (2002) on stability limits
  - Max stable frequency for your wing: ___ Hz
  - Your design frequency: ___ Hz
  - Safe? (YES/NO)

### Week 5–6: Validation Decision

- [ ] Do all simulation results look reasonable?
  - (YES → proceed to Phase 1 build decision)
  - (NO → go to "Week 7–8: Refinement")

- [ ] Do you have access to a wind tunnel or CFD?
  - (YES → consider Tier 2 validation, see tools_guide.md)
  - (NO → skip CFD, proceed with results as-is)

### Week 7–8: Refinement (If Needed)

- [ ] Problem: Thrust too low
  - Action: Increase stroke amplitude in `00_insect_biomechanics/sim.py` STROKE_AMP_DEG
  - Re-run Module 02
  - Record new T/W: ___

- [ ] Problem: Control unstable (phase margin < 30°)
  - Action: Increase damping or reduce bandwidth in `06_flight_dynamics/sim.py`
  - Adjust PID gains
  - Re-run and check Bode plot

- [ ] Problem: Simulation doesn't match literature
  - Action: Run OpenFOAM (Tier 2) for one design point
  - Compare CFD thrust to Whitney & Wood
  - If different > 20%: update your model

### Final Gate: Phase 0 Done

- [ ] All modules PASS evaluator? (YES/NO)
- [ ] T/W ratio ≥ 1.5? (YES/NO)
- [ ] Control bandwidth ≥ 20 Hz? (YES/NO)
- [ ] Power budget ≤ 100 mW? (YES/NO)

**If all YES**: Proceed to Phase 1 decision

**If any NO**: Either (a) redesign in simulation, or (b) accept risk and build anyway

---

## Phase 1: Bench Prototype Decision

### Before You Order Parts

- [ ] Read `plan/build_guide.md` (30 min)
- [ ] Do you have:
  - [ ] Access to a laser cutter (for wings) or makerspace?
  - [ ] Access to 3D printer (SLA/FDM) or can order prints online?
  - [ ] Budget: $500–1,500?
  - [ ] Time: 8–12 weeks?
  - [ ] Indoor space for testing (2 m × 2 m × 2 m clear)?
  - [ ] Willingness to debug (expect it to fail 3–5 times)?

- [ ] Component sourcing
  - [ ] PZT actuators: ordered? (cost: $200–400)
  - [ ] Wings: design finalized for laser cutting?
  - [ ] Electronics: PCB design started or off-the-shelf kit selected?
  - [ ] Battery: purchased? (50 mAh Li-poly)

---

## Phase 1: Build (Weeks 9–18, parallel with Phase 0)

### Weeks 1–2: Mechanical Assembly

- [ ] Wings fabricated (laser-cut carbon fiber or 3D printed)
  - Mass per wing: ___ mg
  - Stiffness verified? (bend test, note the deflection)

- [ ] Body 3D printed
  - Mass: ___ mg
  - CoG balance check: balanced on razor blade edge? (YES/NO)

- [ ] Actuators bonded to wing roots
  - Epoxy type: _______________
  - Cure time: ___ hours
  - Pull test: wings move when gently tugged? (YES/NO)

- [ ] Total mass: ___ mg (target: < 10 mg for first prototype)

### Weeks 3–4: Electronics

**Option A: Tethered (Recommended First)**
- [ ] Function generator borrowed or purchased
- [ ] Power amplifier (0–30 V, 1 A) available
- [ ] Piezo bimorphs wired to amplifier output
- [ ] Test with low voltage (5 V, 100 Hz) — wings move? (YES/NO)

**Option B: Wireless**
- [ ] STM32L151 MCU programmed with firmware
- [ ] nRF52 BLE module tested (mobile app controls)
- [ ] Motor driver (DRV8833) board soldered
- [ ] Custom PCB manufactured and assembled
- [ ] Wireless range tested: ___ meters

### Weeks 5–6: Static Thrust Test

- [ ] Load cell (50 g capacity) mounted on stand
- [ ] Robot tethered to load cell via thin monofilament
- [ ] Function generator sweeping 50–300 Hz
- [ ] Data collected:

| Frequency (Hz) | Thrust (mg) | Notes |
|---|---|---|
| 50 | ___ | |
| 100 | ___ | |
| 150 | ___ | |
| 200 | ___ | |
| 250 | ___ | |
| 300 | ___ | |

- [ ] Peak thrust: ___ mg (target: > 10 mg at design frequency)
- [ ] Compare to simulation: within ±30%? (YES/NO/UNKNOWN)
  - If NO: Debug (wing flexibility, epoxy bond, actuator efficiency)

### Weeks 7–8: Tethered Dynamic Test

- [ ] Clear indoor space: 2 m × 2 m × 2 m (gymnasium, lab, hangar)
- [ ] Monofilament tether attached to robot, led to overhead force sensor
- [ ] Wireless control enabled or signal generator connected
- [ ] Slow-motion video (iPhone 240 fps) recording:
  - Wing beat frequency: ___ Hz (target: 200 Hz)
  - Stroke amplitude: ___ ° (target: ±60°)
  - Symmetry left/right: symmetric? (YES/NO)

- [ ] IMU data logged (if equipped):
  - Roll rate: ___ °/s (should be low for hovering)
  - Pitch rate: ___ °/s
  - Yaw rate: ___ °/s

- [ ] Control response:
  - Does pitch change when you adjust asymmetric wing amplitude? (YES/NO)
  - Latency: ___ ms (should be < 100 ms)

### Weeks 9–10: Free Flight

- [ ] Reduce tether diameter gradually:
  - Week 9a: 0.5 mm monofilament (can support weight)
  - Week 9b: 0.3 mm monofilament (can't support weight, emergency catch only)
  - Week 9c: Remove tether, open flight

- [ ] First free flight indoors:
  - Duration: ___ seconds (target: > 5 seconds)
  - Stable hover? (YES/NO)
  - Drifted or descended? (describe)

- [ ] Iteration based on observations:
  - Drifts left/right → adjust yaw controller
  - Dives forward → adjust pitch
  - Falls like rock → thrust insufficient, return to Phase 0

### Final Gate: Phase 1 Done

- [ ] Robot hovers freely for > 5 seconds? (YES/NO)
- [ ] Thrust matches simulation (±30%)? (YES/NO)
- [ ] Battery lasts > 5 minutes? (YES/NO)
- [ ] Control is responsive (< 100 ms latency)? (YES/NO)

**If all YES**: Phase 0 simulation was validated, proceed to Phase 2 planning

**If any NO**: Document what broke, update Phase 0 sim, iterate

---

## Phase 2: MEMS Fabrication (If Proceeding)

### Design Prep (Weeks 1–4)

- [ ] Finalize wing design from Phase 1 validation
- [ ] Create GDS-II layout files (using gdstk)
  - [ ] Wing pattern: `design/mems_layout/wing_pattern_v1.py` runs
  - [ ] Actuator array: `design/mems_layout/actuator_array_v1.py` runs
  - [ ] Body outline: `design/mems_layout/body_profile_v1.py` runs

- [ ] Design Rule Check (DRC):
  - [ ] All features within foundry minimum (typically 2–5 µm)
  - [ ] No spacing violations
  - [ ] Layer assignments correct

- [ ] Generate documents:
  - [ ] `design/spec_sheet.md` (performance targets)
  - [ ] `design/fabrication_traveler.md` (process flow)
  - [ ] `design/bom.md` (bill of materials)
  - [ ] `design/test_protocol.md` (validation plan)

### Foundry Selection (Week 5)

- [ ] Research options:
  - Sandia SUMMIT V? (16 weeks, $50–100k)
  - SiTime MEMS+ ? (12 weeks, $50–200k)
  - MIT.nano / Stanford SNF? (8 weeks, $1–2k labor, academic)
  - Commercial foundry (China)? (12 weeks, $20–80k, higher risk)

- [ ] Selected foundry: _______________
- [ ] Contact: received DFM review feedback? (YES/NO)
- [ ] Cost estimate: $_______________
- [ ] Lead time: ___ weeks

### Fabrication (Weeks 6–20)

- [ ] GDS-II files submitted
- [ ] Process traveler finalized with foundry
- [ ] Photomask tooling complete (weeks 6–10)
- [ ] Wafer run starts (week 11)
- [ ] Wafer run completes (weeks 11–20 depending on foundry)
- [ ] Wafer dicing + QA complete (weeks 18–20)
- [ ] First die received for testing

### First MEMS Flight (Weeks 21–24)

- [ ] Integrate MEMS body with off-the-shelf electronics
- [ ] Calibrate sensors, tune control gains (based on Phase 1 data)
- [ ] Tethered flight test (validate resonance frequencies, thrust)
- [ ] Free flight in wind tunnel
- [ ] Autonomous indoor flight demo

### Final Gate: Phase 2 Done

- [ ] MEMS robot flies autonomously indoors? (YES/NO)
- [ ] Matches Phase 1 performance (within margin)? (YES/NO)
- [ ] Design proven ready for mass fabrication? (YES/NO)

---

## Documentation Checklist

- [ ] All Phase 0 results saved (*.png plots, *.md results)
- [ ] All Phase 1 test data saved (load cell data, video, IMU logs)
- [ ] Phase 2 GDS-II files backed up
- [ ] Design history documented (changes made, why)
- [ ] Ready for publication or foundry handoff

---

## Publications & Presentation

- [ ] Results match published benchmarks (Dickinson, Whitney & Wood)?
- [ ] Novel contribution identified (what's new vs. prior work)?
- [ ] Ready to write technical paper? (Phase 1 + Phase 2 data)
- [ ] Conference presentation planned?

---

## Legend

- [ ] = checkbox (mark when done)
- YES/NO = decision point
- ___ = fill in your data

---

## Quick Status Overview

```
Phase 0 Status:  ✓ Weeks 1–2  ✓ Weeks 3–4  ☐ Weeks 5–8
Phase 1 Status:  ☐ Weeks 1–2  ☐ Weeks 3–4  ☐ Weeks 5–10
Phase 2 Status:  ☐ Weeks 1–5  ☐ Weeks 6–20 ☐ Weeks 21–24

Legend: ✓ = done, ☐ = pending
```

---

**Good luck! Mark your progress as you go.** 🚁
