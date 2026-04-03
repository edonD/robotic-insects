# Quick Start — Robotic Insects Project

## 5-Minute Setup

```bash
# 1. Install Python dependencies
cd robotic-insects
pip install -r requirements.txt

# 2. Run Wave 1 simulations (foundation)
python 00_insect_biomechanics/sim.py
python 01_actuator_design/sim.py

# 3. Check progress
python evaluate_all.py
```

---

## What This Does

1. **Module 00** simulates fruit fly wing kinematics and muscle dynamics
2. **Module 01** evaluates piezoelectric actuator suitability
3. **evaluate_all.py** grades everything against published benchmarks

---

## Expected Output

```
WAVE 1: Foundations
- 00_insect_biomechanics/results.md   ✓ PASS
- 01_actuator_design/results.md       ✓ PASS

Ready for WAVE 2 (aerodynamics, power, electronics, structures)
```

---

## Full Project Timeline

| Wave | Modules | Focus | Time |
|---|---|---|---|
| **1** | 00–01 | Biomechanics, actuators | 1 hour |
| **2** | 02–05 | Aerodynamics, power, control, structures | 3 hours |
| **3** | 06–07 | Flight control, swarm coordination | 2 hours |
| **4** | 08–09 | Fabrication plan, full integration | 1 hour |
| **Phase 2** | design/ | Spec sheet, layouts, BOM, testing | 2 hours |

**Total**: ~9 hours for complete design framework

---

## Key Files to Read

- **README.md** — Full project overview (read this first)
- **requirements/README.md** — Software installation guide
- **design/spec_sheet.md** — Final performance specification
- **design/test_protocol.md** — How to validate the robot

---

## Next Steps

1. Read **README.md** for project philosophy
2. Follow **requirements/01_python.md** to install packages
3. Run **00_insect_biomechanics/sim.py**
4. Open **biomechanics.png** to see wing kinematics plots

---

## Get Help

- Stuck on a module? Check its `requirements.md`
- Want to see what a previous module produced? Read its `results.md`
- Need to understand grading? Run `/evaluator.py` in any module

---

**Ready?** Start with:
```bash
python 00_insect_biomechanics/sim.py
```

Go! 🚀
