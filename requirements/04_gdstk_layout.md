# MEMS Layout Generation (gdstk)

Module **design/mems_layout** uses `gdstk` to generate photomask layouts in GDS-II format. This is for Phase 2 (after all simulations pass).

---

## Install gdstk

```bash
pip install gdstk
```

Verify:
```python
import gdstk
print(f"gdstk {gdstk.__version__} installed")
```

---

## What gdstk Does

`gdstk` is a Python library for creating MEMS/IC photomask designs:

1. **Wing vein pattern**: Exoskeleton stiffness ribs
2. **Actuator array**: Piezo or shape-memory alloy positions
3. **Body outline**: Overall insect profile

Output files can be sent directly to a MEMS foundry.

---

## Example: Generate a Simple Mask

Create `test_layout.py`:

```python
import gdstk

# Create a cell (like a "layer" in CAD)
cell = gdstk.Cell("RoboInsect_v1")

# Add a rectangle (for wing outline)
rect = gdstk.rectangle((0, 0), (3000, 1000))  # dimensions in nm
cell.add(rect)

# Save as GDS-II
gdstk.write_gds("roboinsect_v1.gds")
print("✓ Mask saved: roboinsect_v1.gds")
```

Run:
```bash
python test_layout.py
```

You should see `roboinsect_v1.gds` created.

---

## Next Steps

Once all Wave 1–4 simulations pass:
1. Run `design/mems_layout/wing_pattern_v1.py`
2. Run `design/mems_layout/actuator_array_v1.py`
3. Run `design/mems_layout/body_profile_v1.py`
4. Send `.gds` files to foundry

---

## ✓ All Software Ready

Go back to main `README.md` and start **Wave 1: Biomechanics & Actuators**.
