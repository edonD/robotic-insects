# FEM Solver for Structural Analysis

Module **05_structural_design** uses FEM to analyze body stiffness, resonance frequencies, and stress distribution.

---

## Install Elmer FEM

### Windows

1. Download installer from [elmerfem.org](https://www.csc.fi/web/elmer/downloads)
2. Run the `.exe` installer
3. Choose installation directory (default is fine)
4. Verify by opening Command Prompt:
   ```bash
   ElmerSolver -help
   ```

### macOS

```bash
brew install elmer
```

### Linux (Ubuntu)

```bash
sudo apt-get install elmer
```

---

## FreeCAD (for 3D Geometry)

Module **05_structural_design** includes a `geometry.FCStd` file (FreeCAD 3D model).

### Installation

- **Windows**: Download from [freecadweb.org](https://www.freecadweb.org/downloads.php)
- **macOS**: `brew install freecad`
- **Linux**: `sudo apt-get install freecad`

### Verification

1. Open FreeCAD
2. File → Open → `05_structural_design/geometry.FCStd`
3. You should see a robotic insect body outline

---

## Export FEM Setup to Elmer

The project includes a Python script to:
1. Read the FreeCAD geometry
2. Generate an Elmer `.sif` input file
3. Run Elmer FEM

This is automated in module **05_structural_design/sim.py**.

---

## Quick Test

Run the structural analysis module:

```bash
python 05_structural_design/sim.py
```

Expected output:
```
Loading geometry from FreeCAD...
Generating Elmer mesh...
Running FEM solver...
Natural frequencies (Hz): [145.2, 287.5, 502.1]
Stress distribution: max 12.4 MPa
✓ Structure passes evaluation
```

---

## Next: MEMS Layout Generation

Proceed to **04_gdstk_layout.md** for mask design tools.
