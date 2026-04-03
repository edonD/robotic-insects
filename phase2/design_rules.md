# Phase 2: MEMS Design Rules (DRC) — RoboInsect v1.0

**Process Node**: 50 µm MEMS  
**Technology**: Silicon + PZT + Ti/Au metallization  
**Revision**: v1.0 (2026-04-03)

---

## Design Rule Summary Table

| Rule ID | Rule Name | Min/Max | Value | Unit | Layer(s) | Rationale |
|---|---|---|---|---|---|---|
| **FE.1** | Minimum feature width | Min | 3 | µm | All | 50 µm process node capability; photolithography resolution limit |
| **FE.2** | Minimum spacing | Min | 3 | µm | All | Prevent bridges during litho + etch; E-beam resolution |
| **EL.1** | Electrode inset from body | Min | 1000 | µm | Electrode | Avoid fringing capacitance; electrical isolation margin |
| **EL.2** | Bond pad size | Min | 150 × 150 | µm | Bond pad | Wire bonding head footprint (typical 150 µm); thermal compression bonding |
| **EL.3** | Bond pad pitch | Min | 300 | µm | Bond pad | Avoid solder bridges; keep spacing adequate for flip-chip assembly |
| **EL.4** | Via-to-edge spacing | Min | 50 | µm | Via | Prevent metal undercut during etch |
| **EL.5** | Metal line width (traces) | Min | 5 | µm | Metal | Sufficient cross-section for current (~1 mA/µm² safe) |
| **CA.1** | Cavity aspect ratio | Max | 20:1 | - | DRIE cavity | DRIE lag effect; deeper cavities need wider features |
| **CA.2** | Cavity corner radius | Min | 10 | µm | DRIE cavity | Avoid sharp re-entrant angles (DRIE scalloping + mask lag) |
| **CA.3** | Cavity depth | Target | 400 ± 20 | µm | DRIE cavity | Thorax cavity for hinge articulation; specified from Module 05 |
| **HI.1** | Hinge flexure width | Min | 100 | µm | Hinge | Structural stiffness; avoid fracture under 10 mN load |
| **HI.2** | Hinge length | Min | 500 | µm | Hinge | Cantilever beam; sufficient for wing deflection |
| **HI.3** | Hinge thickness | Target | 500 | µm | Hinge (substrate depth) | Full substrate thickness for maximum stiffness |
| **IC.1** | Interconnect spacing | Min | 10 | µm | Metal + via | Electromigration margin; voltage <5V operation |
| **IC.2** | Via diameter | Min | 10 | µm | Via | Contact pad size vs. underlying feature alignment |
| **RE.1** | Reticle field size | Max | 30 × 20 | mm | Global | Standard stepper reticle for 4" wafer |
| **RE.2** | Dicing street width | Min | 100 | µm | Dicing keepout | 200 µm blade width + 50 µm safety margin each side |
| **RE.3** | Edge exclusion zone | Min | 3 | mm | Global | Wafer handling; avoid damage from chuck/clamp |
| **CH.1** | Chamfer on re-entrant corners | Angle | 45° | degrees | DRIE cavity | DRIE lag mitigation; prevents sharp stress concentration |
| **ER.1** | Etch selectivity (Si/SiO2) | Min | 50:1 | - | DRIE | SF6/C4F8 Bosch process selectivity |

---

## Detailed Rule Descriptions

### Lithography & Feature Size

**FE.1: Minimum Feature Width** (3 µm)
- **Applies to**: All layers (body outline, electrodes, vias, traces)
- **Equipment**: 365 nm (g-line) photolithography; 0.35 µm minimum CD with best-case optical proximity correction (OPC)
- **Process impact**: Features <3 µm risk incomplete development or collapse during etch
- **Verification**: CD-SEM after litho, pre-etch

**FE.2: Minimum Spacing** (3 µm)
- **Applies to**: All features on same layer; metal-to-metal, contact-to-contact
- **Rationale**: Prevent bridging during resist development or metal deposition
- **Process impact**: Spacing <3 µm during E-beam evaporation may cause unintended continuity
- **Verification**: SEM inspection, electrical continuity test

---

### Electrode & Contact Design

**EL.1: Electrode Inset from Body Edge** (≥1000 µm)
- **Applies to**: PZT top electrode (Layer 20) relative to body outline (Layer 1)
- **Rationale**: Prevents fringing fields; ensures electrical isolation from body edge. 1 mm inset provides:
  - 200 µm safety margin to etch undercut
  - 800 µm field-free zone for mechanical stress relief
- **Verification**: Overlay check (mask-to-mark) ±100 µm tolerance

**EL.2: Bond Pad Size** (≥150 × 150 µm)
- **Applies to**: All wire bond contact pads
- **Rationale**: Standard wire bonding head footprint is 100–150 µm; larger pad reduces contact stress
- **Process impact**: Pads <150 µm risk incomplete wetting with solder or bonding wire
- **Verification**: Optical inspection, pull test on witness samples

**EL.3: Bond Pad Pitch** (≥300 µm)
- **Applies to**: Center-to-center spacing between adjacent bond pads
- **Rationale**: Standard wire bond tool minimum pitch; prevents solder bridges in array bonding
- **Verification**: Dimensional SEM after metallization

**EL.4: Via-to-Edge Spacing** (≥50 µm)
- **Applies to**: Contact holes / vias relative to underlying metal features
- **Rationale**: Metal undercut during via etch (10–50 µm typical) must not expose underlying traces
- **Process impact**: Undercut <50 µm margin risks electrical opens in interconnect
- **Verification**: Cross-section SEM

**EL.5: Metal Line Width (Traces)** (≥5 µm)
- **Applies to**: Interconnect traces, electrode fan-out lines
- **Rationale**: Current density safety (~1 mA/µm² for Au at <100°C); electromigration margin
- **Verification**: Optical inspection, electrical IV test

---

### Deep Reactive Ion Etching (DRIE)

**CA.1: Cavity Aspect Ratio** (≤20:1)
- **Applies to**: DRIE cavity depth ÷ minimum cavity feature width
- **Example**: 400 µm depth ÷ 20 µm minimum feature = 20:1 (at limit)
- **Rationale**: DRIE lag effect: deeper features etch more slowly due to ion density depletion
- **Process impact**: Aspect ratios >20:1 result in non-uniform etch; sloped sidewalls
- **Mitigation**: Increase minimum feature width, or accept ±30% depth tolerance
- **Verification**: SEM cross-section and 3D profilometer

**CA.2: Cavity Corner Radius** (≥10 µm)
- **Applies to**: All re-entrant corners in DRIE cavity (cavity edges, hinge attachment points)
- **Rationale**: Sharp corners create stress concentration + DRIE scalloping artifacts
- **Recommendation**: Use 45° chamfer (10–20 µm radius) at all convex/concave transitions
- **Verification**: SEM of cavity sidewalls

**CA.3: Cavity Depth Target** (400 ± 20 µm)
- **Applies to**: Thorax cavity depth specification (from Module 05 structural design)
- **Process control**: Etch time calibration on test wafer to achieve target ± tolerance
- **Verification**: Profilometer depth scan at 5 locations per wafer

---

### Mechanical Structures (Hinges, Flexures)

**HI.1: Hinge Flexure Width** (≥100 µm)
- **Applies to**: Wing hinge attachment flexures (Layer 3 in body profile)
- **Rationale**: Cantilevered beam under wing deflection load (~10 mN); 100 µm width provides:
  - Second moment: I ≈ w³/12 ≈ 833 µm⁴
  - Deflection: δ = (10 mN) × L³ / (3EI) ≈ acceptable <1 mm @ 500 µm length
- **Verification**: FEA stress analysis + mechanical deflection test

**HI.2: Hinge Length** (≥500 µm)
- **Applies to**: Wing hinge attachment length (structural depth along wing axis)
- **Rationale**: Sufficient for wing deflection range (±5° swing at 200 Hz requires ~50–100 µm peak deflection)
- **Verification**: Mechanical test (gentle push with probe; should deflect smoothly)

**HI.3: Hinge Thickness** (Full substrate = 500 µm)
- **Applies to**: Vertical thickness of hinge flexure (limited by substrate thickness)
- **Rationale**: Use full substrate for maximum bending stiffness (EI ∝ thickness³)
- **Constraint**: Cannot increase thickness beyond substrate without additional deposition steps
- **Verification**: SEM cross-section of hinge sidewall

---

### Interconnect & Contact Design

**IC.1: Interconnect Spacing** (≥10 µm)
- **Applies to**: Traces, vias, metal-to-metal spacing on same layer or adjacent layers
- **Rationale**: Electromigration safety at <5V, <100°C; prevents shorts under thermal stress
- **Verification**: Electrical continuity test (no unexpected shorts)

**IC.2: Via Diameter** (≥10 µm)
- **Applies to**: Contact holes connecting metal layers or to underlying features
- **Rationale**: Contact area for wire bonding or flip-chip; minimum achievable with 365 nm litho + etch
- **Verification**: SEM of via sidewall; electrical contact resistance <1 Ω

---

### Reticle & Die Layout

**RE.1: Reticle Field Size** (≤30 × 20 mm)
- **Applies to**: Total GDS-II layout footprint per reticle exposure
- **Rationale**: Standard stepper exposure field for 4" wafer processing
- **Implication**: Multiple dies per exposure; dicing into individual units
- **Verification**: GDS-II boundary layer check

**RE.2: Dicing Street Width** (≥100 µm)
- **Applies to**: Keepout zone width between adjacent die
- **Rationale**: 200 µm diamond blade width + 50 µm safety margin on each side
- **Purpose**: Prevent blade damage to adjacent die corners during singulation
- **Verification**: Dicing street dimension check on GDS-II

**RE.3: Edge Exclusion Zone** (≥3 mm from wafer edge)
- **Applies to**: No features allowed within 3 mm of wafer perimeter
- **Rationale**: Wafer chuck/clamp grip area; risk of mechanical damage
- **Verification**: GDS-II boundary check + visual wafer inspection

---

### DRIE Process Control

**CH.1: Chamfer on Re-entrant Corners** (45° angle, 10–20 µm radius)
- **Applies to**: All concave corners in DRIE cavity (hinge attachment, cavity edges)
- **Rationale**: Prevents DRIE lag at sharp corners; reduces stress concentration
- **Implementation**: Design cavity with 45° bevel or round corners (minimum 10 µm radius)
- **Verification**: SEM inspection of corner geometry

**ER.1: Etch Selectivity (Si/SiO2)** (≥50:1)
- **Applies to**: SF6/C4F8 Bosch process ratio for DRIE
- **Rationale**: Oxide acts as etch stop for cavity bottom; 50:1 selectivity provides:
  - 400 µm Si etch → <8 µm SiO2 undercut (acceptable)
  - Margin for process variation ±30%
- **Process control**: Monitor etch byproduct emission (Au/Si ratio); adjust SF6/C4F8 cycle time
- **Verification**: SEM cross-section; oxide thickness post-DRIE

---

## Design Rule Hierarchy (Priority)

**Critical Rules** (no exceptions):
- FE.1, FE.2 — Minimum feature size (process capability limit)
- ER.1 — Etch selectivity (process requirement)
- RE.1, RE.3 — Reticle bounds, edge exclusion (tooling constraint)

**High-Priority Rules** (rare exceptions with analysis):
- EL.2, EL.3 — Bond pad size/pitch (assembly requirement)
- HI.1, HI.3 — Hinge width/thickness (mechanical function)
- CA.1, CA.2 — Cavity aspect ratio, corner radius (process yield)

**Recommended Guidelines** (flexible with justification):
- EL.1, EL.4, EL.5 — Electrode/interconnect margins (signal integrity)
- IC.1, IC.2 — Interconnect spacing (reliability)

---

## DRC Checking Methodology

**Tools**: gdstk (Python GDS-II library) or Calibre (commercial)

**Automated checks**:
1. Min width per layer (polygon width ≥ 3 µm)
2. Min spacing per layer (polygon spacing ≥ 3 µm)
3. Electrode-to-body inset (Layer 20 ≥ 1000 µm from Layer 1 edge)
4. Bond pad dimensions (Layer 20 pads ≥ 150 × 150 µm)
5. Reticle bounds (all geometry within ±15 mm × ±10 mm)
6. Edge exclusion (no geometry within 3 mm of wafer edge)

**Manual reviews**:
- Hinge geometry verification (FEA stress check)
- Corner chamfer inspection (visual SEM)
- Overall layout symmetry and alignment

---

**Design Rules Version**: Phase 2 v1.0 (2026-04-03)  
**Approval**: TBD (foundry engineering review)  
**Next step**: Run DRC on GDS-II masks before mask ordering
