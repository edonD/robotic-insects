#!/usr/bin/env python3
"""
Wing Pattern Layout Generator
==============================

Generates GDS-II photomask for robotic insect wing structure.
Output: wing_pattern_v1.gds (send to foundry)
"""

import gdstk

# Create a new GDS-II file
lib = gdstk.GdsLibrary()

# Create a cell (like a layer in CAD)
cell = lib.new_cell("WingPattern_v1")

# Wing outline: Drosophila-scale wing
# Dimensions: 3mm span × 1mm chord
wing_body = gdstk.rectangle(
    (0, 0),           # lower-left (nm)
    (3000000, 1000000),  # upper-right: 3000 µm × 1000 µm
    layer=10          # Layer 10 = wing structure
)
cell.add(wing_body)

# Wing vein pattern (ribs for stiffness)
# Veins run spanwise (along length)
for i in range(5):
    x = 600000 * (i + 1)  # 600 µm spacing
    vein = gdstk.rectangle(
        (x, 0),
        (x + 50000, 1000000),  # 50 µm wide veins
        layer=10
    )
    cell.add(vein)

# Save to GDS-II
gdstk.write_gds("wing_pattern_v1.gds", lib)
print("✓ Generated: wing_pattern_v1.gds")
print("  - Wing outline: 3mm × 1mm")
print("  - 5 structural veins (50 µm wide)")
print("  - Ready for photolithography")
