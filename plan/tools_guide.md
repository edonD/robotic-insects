# Tools Installation & Usage Guide

This guide covers the software needed for Phase 0 (Simulation) and optional advanced tools.

---

## Tier 1: Required (Phase 0 Path A — Python Only)

### Python 3.9+

```bash
# Windows / macOS / Linux
python --version  # Should be 3.9 or later
```

### Scientific Stack

```bash
pip install numpy scipy matplotlib
pip install python-control  # For Bode plots, transfer functions
pip install allantools      # For Allan deviation (optional)
```

Verify:
```python
import numpy as np
import scipy
import matplotlib
import control
print("✓ All required packages installed")
```

**Time to install**: 5 minutes  
**Cost**: Free

---

## Tier 2: Recommended (Path B Validation)

Add CFD validation with XFOIL and simplified OpenFOAM.

### XFOIL (Airfoil Polars)

**What it does**: Computes 2D lift/drag at various angles of attack and Reynolds numbers.  
**Why you need it**: Generates polars that feed into blade-element calculations.

#### Installation

**Windows (WSL2 recommended):**
```bash
# Inside WSL2 Ubuntu terminal
sudo apt-get install xfoil
xfoil  # launches interactive terminal
quit   # exit
```

**macOS:**
```bash
brew install xfoil
```

**Linux:**
```bash
sudo apt-get install xfoil
```

**Verify:**
```bash
xfoil << EOF
LOAD yourwing.dat
OPER
RE 500        # Reynolds number = 500
ALFA 5        # Angle of attack = 5°
DUMP dump.txt # Save results
QUIT
EOF
```

**Time**: 10 minutes  
**Cost**: Free (open-source)  
**Learning curve**: Medium (command-line interface is dated)

---

### OpenFOAM (CFD Solver)

**What it does**: Solves Navier-Stokes equations (unsteady incompressible flow).  
**Why you need it**: Captures leading-edge vortex and unsteady effects that quasi-steady models miss.  
**When to use**: After Path A gives good results, validate 1–2 wing configurations with CFD.

#### Installation (Path: Use WSL2 + Ubuntu)

**Step 1: Install WSL2**
```powershell
# Windows PowerShell (Admin)
wsl --install
# Restart, then launch Ubuntu terminal
```

**Step 2: Inside Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install openfoam-dev paraview

# Verify
foamVersion
```

**Step 3: Create case directory**
```bash
mkdir -p ~/OpenFOAM_Wing
cd ~/OpenFOAM_Wing
# Copy tutorial case
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/airFoil2D .
```

**Time**: 30 minutes (WSL2) + 20 minutes (OpenFOAM)  
**Cost**: Free  
**Learning curve**: High (Navier-Stokes, mesh generation, solver tuning)

**Typical workflow**:
```
1. Define geometry (wing profile, domain)  → Salome meshing
2. Set boundary conditions (inlet, wall, outlet)  → blockMeshDict
3. Run solver  → simpleFoam  or  pimpleFoam
4. Visualize  → paraFoam
5. Compare to Whitney & Wood model
```

**Time per wing condition**: 4–8 hours (mesh + solve + analysis)

---

## Tier 3: Advanced (Path C — Full Co-simulation)

Add structural + dynamics coupling.

### Elmer FEM

**What it does**: Finite element solver for structures, thermal, electromagnetics.  
**Why you need it**: Compute wing resonance frequency, stress under aero loads, thermal management.

#### Installation

**Windows:**
Download from [elmerfem.org](https://www.csc.fi/web/elmer)  
Click `.exe` installer, follow prompts.

**macOS:**
```bash
brew install elmer
```

**Linux (Ubuntu):**
```bash
sudo apt-get install elmerfem
```

**Verify:**
```bash
ElmerSolver -help
```

**Time**: 15 minutes  
**Cost**: Free

---

### MuJoCo (Multi-body Dynamics)

**What it does**: Physics engine for rigid + compliant bodies, contact, constraints.  
**Why you need it**: Simulate full robot dynamics (pitch/roll/yaw) + wing flex effects.

#### Installation

```bash
pip install mujoco
```

**Verify:**
```python
import mujoco
import mujoco.viewer
print(f"MuJoCo {mujoco.__version__}")
```

**Time**: 5 minutes  
**Cost**: Free (academic license)

**Example: Simulate robot body dynamics**
```python
import mujoco

# Load XML model
model = mujoco.MjModel.from_xml_path("robot.xml")
data = mujoco.MjData(model)

# Run 100 time steps
for _ in range(100):
    mujoco.mj_step(model, data)
    print(f"Roll: {data.xquat[1]:.3f}")  # Quaternion
```

---

## Tier 4: Optional (Advanced Analysis)

### FEniCS (Finite Element Library)

Use if you want to implement custom FSI (fluid-structure interaction) coupling.

```bash
pip install fenics-dolfinx
```

**Learning curve**: Very high (PDE solvers, custom variational forms)  
**When to use**: Only if you're doing research-level work

---

## Which Path Should You Use?

### Path A (Python only, right now)
- ✓ Fast iteration
- ✓ No installation headaches
- ✓ Can start today
- ✗ Accuracy ±15% (leading-edge vortex effects are approximate)

**Use if**: You're new to flight simulation or want to rapidly iterate designs.

### Path B (Add XFOIL + OpenFOAM)
- ✓ Validate 1–2 designs with CFD
- ✓ Accuracy ±5%
- ✗ Slower (each CFD run takes hours)

**Use if**: Phase 1 prototype flies, or you want to publish results.

### Path C (Add Elmer + MuJoCo)
- ✓ Comprehensive simulation
- ✓ Accounts for wing flex, control coupling
- ✓ Accuracy 95%+
- ✗ Very slow (weeks per design iteration)

**Use if**: Building Phase 2 MEMS design or doing detailed research.

---

## Installation Checklist

### Before You Run Any Simulation

```bash
# Test Python packages
python -c "import numpy, scipy, matplotlib, control; print('✓ OK')"

# Test visualization
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); print('✓ Plots work')"
```

### Before Phase 1 Build

```bash
# (Optional) Test XFOIL
xfoil
# Type "airfoil" commands, verify it runs

# (Optional) Test MuJoCo
python -c "import mujoco; print(f'MuJoCo {mujoco.__version__}')"
```

### Before Phase 2 MEMS Design

```bash
# Verify FEM
ElmerSolver -help

# Verify GDS generation
python -c "import gdstk; print('✓ gdstk installed')"
```

---

## Next Steps

1. **Install Tier 1** (Python + NumPy/SciPy) — TODAY
2. **Run `02_wing_aerodynamics/sim.py`** — see what baseline looks like
3. **Compare to literature** (Whitney & Wood values in comments)
4. **If needed**, install Tier 2 (XFOIL) — run CFD validation

---

## Troubleshooting

### "Module not found" error
```bash
# Ensure virtualenv is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Then reinstall
pip install --upgrade numpy scipy matplotlib python-control
```

### OpenFOAM won't compile
- Use WSL2 (not native Windows) — much easier
- On macOS: use Homebrew, not source compile
- On Linux: use `apt-get`, not source

### XFOIL runs but gives weird numbers
- Check Reynolds number (should be 100–1000 for insects)
- Verify angle of attack range (-10° to +10° typical)
- Use `OPER RE` to set Re, not command line

---

## References

- [NumPy docs](https://numpy.org/doc/stable/)
- [SciPy docs](https://docs.scipy.org/)
- [python-control docs](https://python-control.readthedocs.io/)
- [OpenFOAM tutorials](https://www.openfoam.com/documentation/user-guide/)
- [Elmer documentation](https://www.csc.fi/web/elmer/documentation)
- [MuJoCo documentation](https://mujoco.readthedocs.io/)

---

## Cost Summary

| Tier | Tools | Cost | Time | Accuracy |
|---|---|---|---|---|
| A | Python | $0 | 5 min | ±15% |
| B | A + XFOIL + OpenFOAM | $0 | 1 hour | ±5% |
| C | B + Elmer + MuJoCo | $0 | 1.5 hours | 95%+ |

**All free and open-source** — the only cost is your time.
