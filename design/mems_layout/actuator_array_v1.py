#!/usr/bin/env python3
"""
PZT Actuator Array Layout Generator
===================================

Generates GDS-II photomask for PZT bimorph electrodes and bond pads.
Output: actuator_array_v1.gds (send to foundry)
"""

import gdstk

# Create a new GDS-II file
lib = gdstk.Library()

# Create a cell (like a layer in CAD)
cell = lib.new_cell("ActuatorArray_v1")

# ===== ACTUATOR 1 (Left) =====
# Position: centered at x=-6000, y=0

# Layer 10: PZT film footprint (10,000 um x 5,000 um)
pzt_1 = gdstk.rectangle(
    (-11000, -2500),      # lower-left
    (-1000, 2500),        # upper-right (10,000 um wide, 5,000 um tall)
    layer=10, datatype=0
)
cell.add(pzt_1)

# Layer 20: Ti/Au top electrode (8,000 um x 4,000 um, centered with 1,000 um inset)
electrode_1 = gdstk.rectangle(
    (-10000, -2000),      # inset 1,000 um from body edge
    (-2000, 2000),        # electrode dimensions
    layer=20, datatype=0
)
cell.add(electrode_1)

# Layer 20: Bond pads (200 um x 200 um) - top and bottom
# Top-left pad
pad_1_tl = gdstk.rectangle(
    (-10500, 2200),
    (-10300, 2400),
    layer=20, datatype=1
)
cell.add(pad_1_tl)

# Top-right pad
pad_1_tr = gdstk.rectangle(
    (-1700, 2200),
    (-1500, 2400),
    layer=20, datatype=1
)
cell.add(pad_1_tr)

# Bottom-left pad
pad_1_bl = gdstk.rectangle(
    (-10500, -2400),
    (-10300, -2200),
    layer=20, datatype=1
)
cell.add(pad_1_bl)

# Bottom-right pad
pad_1_br = gdstk.rectangle(
    (-1700, -2400),
    (-1500, -2200),
    layer=20, datatype=1
)
cell.add(pad_1_br)

# Layer 30: Etch release slots (100 um wide at beam ends)
release_1_top = gdstk.rectangle(
    (-10500, 2100),
    (-1500, 2200),
    layer=30, datatype=0
)
cell.add(release_1_top)

release_1_bottom = gdstk.rectangle(
    (-10500, -2200),
    (-1500, -2100),
    layer=30, datatype=0
)
cell.add(release_1_bottom)

# ===== ACTUATOR 2 (Right) =====
# Position: centered at x=+6000, y=0 (mirrored geometry)

# Layer 10: PZT film footprint
pzt_2 = gdstk.rectangle(
    (1000, -2500),        # lower-left
    (11000, 2500),        # upper-right
    layer=10, datatype=0
)
cell.add(pzt_2)

# Layer 20: Ti/Au top electrode
electrode_2 = gdstk.rectangle(
    (2000, -2000),
    (10000, 2000),
    layer=20, datatype=0
)
cell.add(electrode_2)

# Layer 20: Bond pads (symmetrically placed)
pad_2_tl = gdstk.rectangle(
    (1500, 2200),
    (1700, 2400),
    layer=20, datatype=1
)
cell.add(pad_2_tl)

pad_2_tr = gdstk.rectangle(
    (10300, 2200),
    (10500, 2400),
    layer=20, datatype=1
)
cell.add(pad_2_tr)

pad_2_bl = gdstk.rectangle(
    (1500, -2400),
    (1700, -2200),
    layer=20, datatype=1
)
cell.add(pad_2_bl)

pad_2_br = gdstk.rectangle(
    (10300, -2400),
    (10500, -2200),
    layer=20, datatype=1
)
cell.add(pad_2_br)

# Layer 30: Etch release slots
release_2_top = gdstk.rectangle(
    (1500, 2100),
    (10500, 2200),
    layer=30, datatype=0
)
cell.add(release_2_top)

release_2_bottom = gdstk.rectangle(
    (1500, -2200),
    (10500, -2100),
    layer=30, datatype=0
)
cell.add(release_2_bottom)

# Save to GDS-II
lib.write_gds("design/mems_layout/actuator_array_v1.gds")

# Print summary
print("OK: Generated actuator_array_v1.gds")
print("  Layer 10 (PZT film):    2x 10,000 um x 5,000 um")
print("  Layer 20 (Electrode):   2x 8,000 um x 4,000 um (1,000 um inset)")
print("  Layer 20 (Bond pads):   8x 200 um x 200 um (4 per actuator)")
print("  Layer 30 (Release):     4x 100 um slots at beam ends")
print("  Actuator 1 center:      x=-6,000 um, y=0 um")
print("  Actuator 2 center:      x=+6,000 um, y=0 um")
print("  Total span:             +/-11,000 um x +/-2,500 um")
print("  Ready for photolithography mask 2 (electrode) and mask 3 (release)")
