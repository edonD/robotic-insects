# CFD for Wing Aerodynamics

Module **02_wing_aerodynamics** needs a CFD solver to compute lift, drag, and control torques from wing geometry and motion.

---

## Option A: OpenFOAM (Free, Recommended)

OpenFOAM is free and sufficient for insect-scale wing aerodynamics.

### Installation (Windows)

1. Download **Windows Subsystem for Linux 2 (WSL2)**: https://docs.microsoft.com/en-us/windows/wsl/install
2. Inside WSL, run:
   ```bash
   sudo apt-get update
   sudo apt-get install openfoam9
   ```
3. Verify:
   ```bash
   icoFoam -help
   ```

### Installation (macOS/Linux)

```bash
# macOS (using Homebrew)
brew install openfoam

# Ubuntu
sudo apt-get install openfoam9
```

---

## Option B: ANSYS Fluent

If your institution has a license, ANSYS Fluent is more user-friendly but commercial.

1. Install from [ANSYS Student Portal](https://www.ansys.com/en-us/student)
2. Follow ANSYS installation guide
3. Verify: Launch `fluent` from command line

---

## Option C: Simplified Aerodynamic Model (Python)

If you cannot install CFD software, module **02_wing_aerodynamics** includes a simplified analytical model using:
- Blade element theory
- 2D airfoil polars (XFOIL pre-computed)
- Quasi-static thrust prediction

This is less accurate than CFD but sufficient for preliminary design.

---

## Which Option to Choose?

| Option | Cost | Accuracy | Effort |
|---|---|---|---|
| OpenFOAM | Free | Good (80%) | High |
| ANSYS Fluent | $$ | Excellent (95%) | Low |
| Python analytical | Free | Moderate (60%) | Low |

**Recommendation**: Start with Python analytical model. If results are marginal, use OpenFOAM later.

---

## Verification

Run module **02_wing_aerodynamics/sim.py**. It will auto-detect which solver you have and use it, or fall back to analytical.

```bash
python 02_wing_aerodynamics/sim.py
```

If successful, you'll see thrust and drag numbers for a Drosophila-scale wing.

---

## Next: Structural FEM

Proceed to **03_fem_structures.md** for finite element modeling.
