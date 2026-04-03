# MEMS Layout — Photomask Design

This directory contains gdstk Python scripts that generate **GDS-II photomask layouts** for the robotic insect.

---

## Files

- **wing_pattern_v1.py**: Wing vein pattern (structural ribs, dimensions in nm)
- **actuator_array_v1.py**: Piezo actuator placement and routing
- **body_profile_v1.py**: Body outline and leg attachment points

---

## Workflow

1. All Wave 1–4 simulations must **PASS**
2. Run each Python script:
   ```bash
   python wing_pattern_v1.py      # generates wing_pattern_v1.gds
   python actuator_array_v1.py    # generates actuator_array_v1.gds
   python body_profile_v1.py      # generates body_profile_v1.gds
   ```
3. Open `.gds` files in KLayout or send to foundry

---

## GDS-II Output

Each script generates a GDS-II file compatible with industry-standard foundries (ASML, Nikon, Canon mask tooling).

**Scale**: All dimensions in nanometers (nm)

---

## Example: Wing Pattern

```python
# From wing_pattern_v1.py
wing_vein = gdstk.rectangle(
    (0, 0),           # lower-left corner (nm)
    (3000, 1000),     # upper-right corner: 3mm × 1mm
    layer=10          # GDS layer 10
)
```

---

## Deliverables

Once all layouts pass review:
1. Merge `.gds` files into single **roboinsect_combined.gds**
2. Create design rule check (DRC) verification report
3. Submit to MEMS foundry for fabrication

---

**Auto-compiled from Module 08 results**
