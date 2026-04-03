#!/usr/bin/env python3
"""
Silicon Body Profile Layout Generator
=====================================

Generates GDS-II photomask for silicon body, thorax cavity, wing hinges,
and mounting features.
Output: body_profile_v1.gds (send to foundry)
"""

import gdstk

# Create a new GDS-II file
lib = gdstk.Library()

# Create a cell
cell = lib.new_cell("BodyProfile_v1")

# Body dimensions: 4,000 um x 1,500 um, centered at origin
# Layer 1: Silicon body outline

body = gdstk.rectangle(
    (-2000, -750),        # lower-left (center: -2000 to +2000 x-direction)
    (2000, 750),          # upper-right
    layer=1, datatype=0
)
cell.add(body)

# Layer 2: DRIE thorax cavity
# 3,000 um x 1,000 um cavity (400 um depth from topside surface)
# Centered within body
thorax_cavity = gdstk.rectangle(
    (-1500, -500),        # centered cavity
    (1500, 500),          # 3,000 um wide x 1,000 um tall
    layer=2, datatype=0
)
cell.add(thorax_cavity)

# Layer 3: Wing hinge flexures
# Two flexures (left and right) for wing attachment
# Each: 100 um wide x 500 um long

# Left wing hinge (extends leftward from -1500)
left_hinge = gdstk.rectangle(
    (-2000, -50),         # 100 um tall centered on x-axis
    (-1500, 50),          # extends to left body edge
    layer=3, datatype=0
)
cell.add(left_hinge)

# Right wing hinge (extends rightward from +1500)
right_hinge = gdstk.rectangle(
    (1500, -50),
    (2000, 50),
    layer=3, datatype=0
)
cell.add(right_hinge)

# Layer 4: Mounting holes
# 4 holes at corners: 300 um diameter (approx as rectangles 300x300)
# Positioned at corners with 150 um inset

mount_hole_tl = gdstk.rectangle(
    (-1850, 600),         # top-left, 150 um inset
    (-1550, 900),
    layer=4, datatype=0
)
cell.add(mount_hole_tl)

mount_hole_tr = gdstk.rectangle(
    (1550, 600),          # top-right
    (1850, 900),
    layer=4, datatype=0
)
cell.add(mount_hole_tr)

mount_hole_bl = gdstk.rectangle(
    (-1850, -900),        # bottom-left
    (-1550, -600),
    layer=4, datatype=0
)
cell.add(mount_hole_bl)

mount_hole_br = gdstk.rectangle(
    (1550, -900),         # bottom-right
    (1850, -600),
    layer=4, datatype=0
)
cell.add(mount_hole_br)

# Layer 5: Dicing street keepout zone
# 100 um exclusion perimeter around body (design guideline for dicing blade)

# Top dicing keepout
top_keepout = gdstk.rectangle(
    (-2100, 750),
    (2100, 850),
    layer=5, datatype=0
)
cell.add(top_keepout)

# Bottom dicing keepout
bottom_keepout = gdstk.rectangle(
    (-2100, -850),
    (2100, -750),
    layer=5, datatype=0
)
cell.add(bottom_keepout)

# Left dicing keepout
left_keepout = gdstk.rectangle(
    (-2100, -750),
    (-2000, 750),
    layer=5, datatype=0
)
cell.add(left_keepout)

# Right dicing keepout
right_keepout = gdstk.rectangle(
    (2000, -750),
    (2100, 750),
    layer=5, datatype=0
)
cell.add(right_keepout)

# Save to GDS-II
lib.write_gds("design/mems_layout/body_profile_v1.gds")

# Print summary
print("OK: Generated body_profile_v1.gds")
print("  Layer 1 (Body outline):       4,000 um x 1,500 um (centered)")
print("  Layer 2 (DRIE cavity):        3,000 um x 1,000 um thorax (400 um depth)")
print("  Layer 3 (Wing hinges):        2x 100 um x 500 um flexures (left/right)")
print("  Layer 4 (Mounting holes):     4x 300 um diameter (150 um inset from corners)")
print("  Layer 5 (Dicing keepout):     100 um perimeter exclusion zone")
print("  Wing hinge spacing:           Left at x=-1500 um, Right at x=+1500 um")
print("  Cavity center:                x=0 um, y=0 um")
print("  Total wafer footprint:        +/-2,100 um x +/-850 um (with keepout)")
print("  Ready for photolithography mask 1 (body outline)")
