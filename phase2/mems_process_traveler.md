# Phase 2: MEMS Process Traveler — RoboInsect v1.0 Silicon Fabrication

**For**: Silicon MEMS Foundry (SiNE, OA Xiamen, or similar)  
**Process Node**: 50 µm MEMS  
**Expected Batch**: 100 units (1/4 wafer share on MPW shuttle)  
**Lead Time**: 8–10 weeks  
**Yield Target**: >80% die yield, <2% delamination rate

---

## Wafer Specification

| Parameter | Value | Units | Notes |
|---|---|---|---|
| Wafer diameter | 4 | inches | Standard 100 mm |
| Substrate material | Si <100> | - | p-type (boron doped) |
| Substrate resistivity | 1–10 | Ω·cm | Typical MBE quality |
| Thickness | 500 | µm | Mechanical strength |
| Surface finish | DSP | - | Double-side polished |
| Crystal orientation | <100> | - | Standard for MBE and DREI |

---

## Material Stack

| Layer | Material | Thickness | Deposition | Target Tolerance | Purpose |
|---|---|---|---|---|---|
| Substrate | Si <100> | 500 µm | Substrate | ±50 µm | Body structure, hinge |
| Oxide | SiO2 | 5 µm | Thermal wet @ 1100°C | ±0.5 µm | Electrical isolation |
| SiN barrier | Si3N4 | 200 nm | LPCVD @ 800°C | ±30 nm | Etch barrier (optional for DRIE selectivity) |
| Actuator | PZT-5H | 100 µm | Epoxy bonded (UV DP460) | ±10 µm | Piezoelectric layer |
| Metallization | Ti/Au | 0.5 µm | E-beam, Ti 100 nm + Au 400 nm | ±50 nm | Electrical contacts, bond pads |

---

## Process Flow (12 Steps)

### Step 1: Substrate Preparation & RCA Clean
**Inputs**: 4" Si <100> wafers, 500 µm, p-type, DSP  
**Process**: RCA Standard clean (SC-1 + SC-2, 70°C, 10 min each)  
**Purpose**: Remove organic and ionic contaminants  
**QA**: Visual inspection (no residue), wettability test  
**Tolerance**: Surface defect density <10 per cm²

---

### Step 2: Thermal Oxidation (SiO2)
**Process**: Furnace oxidation @ 1100°C wet steam, 8 hours  
**Target thickness**: 5 µm ± 0.5 µm  
**Measurement**: Ellipsometry (3 points per wafer minimum)  
**Purpose**: Electrical isolation layer, etch barrier  
**QA**: No pinholes detected by C-V measurement  
**Ramp rate**: 5°C/min (slow ramp to prevent wafer bow)

---

### Step 3: LPCVD Silicon Nitride (Optional Etch Barrier)
**Process**: Low-pressure chemical vapor deposition @ 800°C  
**Target thickness**: 200 nm ± 30 nm  
**Precursors**: SiH2Cl2 + NH3  
**Purpose**: Enhance DRIE selectivity (Si3N4 acts as etch barrier)  
**QA**: Stress measurement (tensile <500 MPa)  
**Notes**: Optional if SiO2 provides sufficient selectivity

---

### Step 4: Photolithography — Mask 1 (Body Outline & Cavity)
**Resist**: Positive photoresist (Shipley S1805 or equivalent), 1.5 µm  
**Mask**: 5-inch chromium-on-glass, 1:1 scale  
**Exposure**: 365 nm (g-line), 100 mJ/cm²  
**Development**: MF-319, 60 sec, RT  
**Post-bake**: 110°C, 60 sec  
**Purpose**: Define body outline and DRIE cavity area  
**QA**: Critical dimension (CD) check ±1 µm on cavity (3000 µm target)

---

### Step 5: Deep Reactive Ion Etch (DRIE) — Bosch Process
**Etchant gas**: SF6 (etch) + C4F8 (passivate), cycled 10 sec / 5 sec  
**Pressure**: 5–10 Pa  
**Power**: 600 W  
**Target depth**: 400 µm ± 20 µm (thorax cavity)  
**Etch rate**: ~3–4 µm/cycle → ~100 cycles (15–20 min)  
**Selectivity**: Si / SiO2 = ~50:1  
**Purpose**: Create freestanding thorax cavity for wing hinge articulation  
**QA**: SEM cross-section (verify smooth walls, no grass), profilometer depth check

---

### Step 6: Resist Stripping & Surface Preparation
**Strip photoresist**: O2 plasma asher or chemical stripper (Acetone + IPA)  
**Clean residue**: RCA SC-1 (hot, 5 min)  
**Dry**: N2 blow-dry  
**Purpose**: Remove resist and etch byproducts  
**QA**: Surface inspection (no carbonaceous residue)

---

### Step 7: PZT-5H Thin Film Bonding
**Actuator material**: PZT-5H film, 100 µm thick, 10 mm × 5 mm pre-cut  
**Adhesive**: 3M DP460 UV epoxy (two-part, 1:1 ratio)  
**Application**: Thin bead (~0.5 mm) on SiO2 surface  
**Clamping pressure**: 3 MPa (light pressure to prevent piezo fracture)  
**Clamp duration**: 30 min initial set  
**UV cure**: 365 nm lamp, 40W, 3 minutes  
**Final cure**: Room temperature 24 hours (full strength)  
**Purpose**: Attach piezoelectric actuation layer to silicon body  
**QA**: Bond line inspection under microscope (no voids >100 µm), thickness uniformity

---

### Step 8: Photolithography — Mask 2 (Electrodes & Bond Pads)
**Resist**: Positive photoresist, 1.2 µm  
**Mask**: Chromium-on-glass, electrode pattern (8 mm × 4 mm electrodes, 200 µm bond pads)  
**Exposure**: 365 nm, 100 mJ/cm² (adjust for epoxy layer absorption)  
**Development**: MF-319, 60 sec  
**QA**: Electrode alignment to body ±100 µm, pad size ±50 µm

---

### Step 9: Ti/Au Metallization (E-beam Deposition)
**Chamber**: E-beam evaporator, high-vacuum (< 5×10⁻⁶ Torr)  
**Deposition sequence**:
  1. Titanium (adhesion layer): 100 nm @ 0.5 Å/sec
  2. Gold (conductor): 400 nm @ 1.0 Å/sec
**Rate monitoring**: Quartz crystal oscillator  
**Temperature**: Room temperature (resist thermal limit)  
**Purpose**: Electrode metallization and bond pad formation  
**QA**: Sheet resistance ~0.05 Ω/square (4-point probe), thickness ±10%

---

### Step 10: Lift-Off & Metal Pattern Definition
**Solvent**: Acetone (warm, ~50°C) or N-Methyl-2-pyrrolidone (NMP) for DP460  
**Soak time**: 30–60 min (DP460 is tough; may require ultrasonic assist 5 min @ 20 kHz)  
**Rinse**: IPA × 2, dry with N2  
**Purpose**: Remove excess metal and photoresist, leaving patterned electrodes  
**QA**: Visual inspection (no metal residue), continuity test (electrode-to-pad)

---

### Step 11: Photolithography — Mask 3 (Release Slots & Etch Stops)
**Resist**: Positive photoresist, 1.5 µm  
**Mask**: Chromium-on-glass, release slot pattern (100 µm slots at hinge ends)  
**Exposure**: 365 nm, 100 mJ/cm²  
**Development**: MF-319, 60 sec  
**Purpose**: Define release etch areas to free moving parts (hinges)  
**QA**: Slot alignment ±50 µm

---

### Step 12: HF Vapor Release Etch (Anisotropic Si Etch)
**Etchant**: 40% HF vapor (heated chamber, ~50°C)  
**Etch time**: 45 min ± 5 min  
**Etch rate**: ~0.2 µm/min (SiO2 in HF vapor)  
**Purpose**: Remove oxide around hinges to create freestanding articulation  
**Caution**: HF is extremely corrosive; use only in proper fume hood with personal monitoring  
**QA**: Mechanical test (gently push hinge with probe — should deflect <100 µm at max load)

---

### Step 13: Dicing & Singulation
**Blade**: Diamond-coated blade, 200 µm width  
**Speed**: 5 mm/sec  
**Coolant**: Deionized water (low contamination)  
**Purpose**: Separate individual die from wafer  
**Dicing street width**: 100 µm keepout (blade cuts between dies)  
**QA**: Visual inspection (no chipping), edge profile SEM (optional)

---

### Step 14: In-Process Inspection & QA

#### Checkpoints:
1. **After step 2 (SiO2)**: Ellipsometry thickness map (5 µm ±0.5)
2. **After step 5 (DRIE)**: Profilometer depth scan (400 µm ±20), SEM cross-section
3. **After step 7 (PZT bonding)**: Optical microscopy (bond voids <5%), thickness measurement
4. **After step 9 (Ti/Au)**: 4-point probe sheet resistance, thickness calibration
5. **After step 12 (HF release)**: Mechanical hinge deflection test, SEM of freestanding hinges
6. **Final (post-dicing)**: Electrical continuity test (all pads), visual inspection

#### Yield Targets:
- **Wafer-level yield**: >85% of processes proceed without catastrophic failure
- **Die yield**: >80% of singulated die pass electrical continuity test
- **Mechanical yield**: >95% of hinges deflect freely (delamination rate <2%)

---

## In-Process Inspection Summary

| Step | Measurement | Target | Equipment |
|---|---|---|---|
| 2 | SiO2 thickness | 5 ± 0.5 µm | Ellipsometer |
| 5 | DRIE cavity depth | 400 ± 20 µm | Profilometer + SEM |
| 7 | PZT bond voids | <5% | Optical microscope |
| 9 | Ti/Au resistance | 0.05 Ω/sq ± 10% | 4-point probe |
| 12 | Hinge deflection | <100 µm @ 10 mN | Manual probe + force gauge |
| 13 | Die continuity | 0 Ω on all pads | Multimeter |

---

## Process Documentation & Files

The following files must accompany this traveler for foundry submission:

1. **GDS-II masks** (3 masks total):
   - `mask_1_body_outline.gds` — body perimeter, thorax cavity, dicing streets
   - `mask_2_electrodes.gds` — PZT electrode pattern, bond pads
   - `mask_3_release_slots.gds` — etch release areas

2. **Layer definition map** (`layer_map.txt`):
   ```
   Layer 1: Silicon body / DRIE cavity boundary
   Layer 2: DRIE cavity (400 µm depth)
   Layer 3: Electrode top surface
   Layer 4: Mounting features
   Layer 5: Dicing keepout
   ```

3. **Process parameter sheet** (this document)

4. **Design rule checklist** (`design_rules.md`)

---

## Known Constraints & Mitigations

| Constraint | Impact | Mitigation |
|---|---|---|
| **HF vapor release uncertainty** | Hinge stiffness may vary ±30% | Calibrate etch rate on test die; provide min/max etch time range |
| **PZT epoxy curing in vacuum** | Outgassing may cause voids | Allow longer room-temp cure (24h) before subsequent steps |
| **DRIE grass on sidewalls** | May increase hinge damping | Use optimized SF6/C4F8 ratio; post-DRIE O2 ash to clean |
| **Au migration in bondpads** | Long-term reliability risk | Use Ti barrier layer; limit storage temperature <60°C |

---

## Foundry Partner Recommendations

**Preferred MPW vendors for this process**:
- **SiNE (Singapore)**: Excellent DRIE selectivity, proven PZT bonding
- **OA Xiamen (China)**: Lower cost, good QA on 50 µm node
- **IMEC (Belgium)**: Premium process, highest yield (for pre-production runs)

**Mask set cost estimate**: $3,000–$8,000 (3 masks, chrome-on-glass)  
**Wafer run cost**: $5,000–$15,000 (1/4 wafer share, 100 die)

---

**Process Traveler Version**: Phase 2 v1.0 (2026-04-03)  
**Compiled from**: Module 08 (Fabrication Plan), design decisions locked in Phase 0  
**Next step**: Design rule check (DRC) and mask ordering
