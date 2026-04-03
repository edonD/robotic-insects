# Phase 2: Foundry Pre-Submission Checklist — RoboInsect v1.0

**Project**: RoboInsect v1.0 Silicon MEMS (Phase 2)  
**Target Foundry**: SiNE, OA Xiamen, or IMEC MPW shuttle  
**Submission Date**: TBD (planned by 2026-05-01)  
**Project Lead**: TBD  
**Approval**: [ ] Design Review [ ] Foundry Review

---

## Section 1: GDS-II File Requirements

### File Format & Structure
- [ ] **File naming**: `roboinsect_v1_mask_1_body.gds`, `mask_2_electrodes.gds`, `mask_3_release.gds`
- [ ] **Unit scale**: Micrometers (µm), no nanometer units
- [ ] **Resolution**: 0.001 µm (1000 dbu/µm)
- [ ] **Top-level cell name**: `BodyProfile_v1`, `ActuatorArray_v1`, `WingPattern_v1`
- [ ] **No undefined cell references** (all cells referenced must be defined in the GDS file)
- [ ] **No off-grid geometry** (all vertices must align to grid points)
- [ ] **Polygon orientation**: Correct (counterclockwise = filled area, clockwise = hole)
- [ ] **No self-intersecting polygons** (run drc_check.py to verify)

### Layer Assignment
- [ ] **Layer 1**: Si body outline (datatype 0)
- [ ] **Layer 2**: DRIE cavity (datatype 0)
- [ ] **Layer 3**: Wing hinges (datatype 0)
- [ ] **Layer 4**: Mounting features (datatype 0)
- [ ] **Layer 5**: Dicing keepout (datatype 0)
- [ ] **Layer 10**: PZT film footprint (datatype 0)
- [ ] **Layer 20**: Electrodes (datatype 0), bond pads (datatype 1)
- [ ] **Layer 30**: Etch release slots (datatype 0)
- [ ] **No layer 0** (reserved, not used)
- [ ] **All layers have descriptions** in layer map document

### File Integrity
- [ ] **File size**: < 10 MB (typical: 100 KB for simple 50 µm MEMS)
- [ ] **Valid GDS-II syntax** (use GDS2 validation tool or Python gdstk)
- [ ] **Checksum verification** (foundry will verify on receipt)
- [ ] **Archive format**: Uncompressed .gds (NOT .zip or .tar.gz for first submission)

---

## Section 2: Design Rule Check (DRC) & Waiver Documentation

### DRC Rules Applied
- [ ] **Minimum feature width** >= 3 µm (all layers): **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Minimum spacing** >= 3 µm (all layers): **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Electrode inset** >= 1000 µm from body edge: **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Bond pad size** >= 150 × 150 µm: **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Bond pad pitch** >= 300 µm: **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **DRIE cavity aspect ratio** <= 20:1: **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Reticle bounds** <= 30 × 20 mm: **Status**: [  ] PASS [  ] FAIL [  ] N/A
- [ ] **Edge exclusion** >= 3 mm from wafer perimeter: **Status**: [  ] PASS [  ] FAIL [  ] N/A

### DRC Report Documentation
- [ ] **DRC report file**: `design/mems_layout/drc_report.json` generated and attached
- [ ] **Number of violations**: < 5 (acceptable for foundry submission)
- [ ] **All critical violations resolved**: Yes [ ] No [ ] (if No, provide waiver justification below)
- [ ] **Waived violations documented**:
  - Violation 1: _____________________________ | Justification: _____________________________
  - Violation 2: _____________________________ | Justification: _____________________________
  - Violation 3: _____________________________ | Justification: _____________________________

### Rule File Documentation
- [ ] **Design rules document**: `phase2/design_rules.md` (describes all 20+ rules)
- [ ] **Rule rationale document**: Provided to foundry
- [ ] **Foundry acknowledgment**: Received and accepted

---

## Section 3: Mask Specification & Ordering

### Mask Set Composition (3 Masks)
1. [ ] **Mask 1 — Body Outline**
   - [ ] GDS file: `mask_1_body_outline.gds`
   - [ ] Layers: Layer 1 (body), Layer 2 (cavity), Layer 3 (hinges), Layer 4 (mounting), Layer 5 (dicing)
   - [ ] Expected features: Body outline (4000 × 1500 µm), cavity (3000 × 1000 µm), hinges

2. [ ] **Mask 2 — Electrodes**
   - [ ] GDS file: `mask_2_electrodes.gds`
   - [ ] Layers: Layer 20 (electrodes, bond pads)
   - [ ] Expected features: 2× 8000 × 4000 µm electrodes, 8× 200 × 200 µm bond pads

3. [ ] **Mask 3 — Release Slots**
   - [ ] GDS file: `mask_3_release_slots.gds`
   - [ ] Layers: Layer 30 (etch release)
   - [ ] Expected features: 4× 100 µm width release slots at hinge ends

### Photomask Specifications
- [ ] **Mask material**: Chrome-on-glass (CoG)
- [ ] **Mask size**: 5-inch (127 mm) or 6-inch standard
- [ ] **Pattern type**: Positive (clear = exposed areas; dark = unexposed)
- [ ] **Minimum feature**: 3 µm
- [ ] **Defect density**: < 0.1 defects per cm² (critical dimension areas)
- [ ] **Line edge roughness (LER)**: < 50 nm (3-sigma)
- [ ] **Optical contrast**: > 90% (transmittance difference clear vs. dark)
- [ ] **Pellicle**: Yes [ ] No [ ] (recommended for <5 µm features)

### GDSII-to-MEBES Conversion
- [ ] **Conversion tool**: Verify compatibility with mask shop (e.g., Mentor Calibre, Synopsys)
- [ ] **Conversion report**: Reviewed for no errors
- [ ] **Fracturing**: Performed correctly (no oversized polygons in MEBES output)
- [ ] **Data integrity check**: Perform reverse-conversion to GDS-II; compare geometry

### Mask Shop Selection
- **Recommended vendors**: 
  - [ ] Photronics Inc. (Rochester, NY) — high-end optical masks
  - [ ] Compugraphics (UK) — fast turnaround
  - [ ] Applied Nanotech (Austin, TX) — cost-effective
- [ ] **Quote obtained**: Cost estimate $ _______  , Lead time: _____ days
- [ ] **Delivery date**: TBD (typically 3–4 weeks after order)

---

## Section 4: Design Review & Cross-Checks

### Design Review Sign-Offs (2 Required)
1. [ ] **Reviewer 1**: _________________________ | Date: _________ | Sign: _________
   - Review scope: GDS geometry, design rules, feature alignment
   - Sign-off: This design is ready for foundry fabrication
   - Comments: _________________________________________________________________

2. [ ] **Reviewer 2**: _________________________ | Date: _________ | Sign: _________
   - Review scope: Process flow, material stack, yield risk assessment
   - Sign-off: Process traveler is complete and feasible at target foundry
   - Comments: _________________________________________________________________

### Cross-Check with Phase 1 (Bench Prototype)
- [ ] **Body dimensions Phase 0 → Phase 2**: 4 × 1.5 mm = 4000 × 1500 µm ✓
- [ ] **Wing hinge length Phase 0 → Phase 2**: 500 µm ✓
- [ ] **Hinge width Phase 0 → Phase 2**: 100 µm ✓
- [ ] **DRIE cavity depth Phase 0 → Phase 2**: 400 µm ✓
- [ ] **PZT actuator size Phase 1 → Phase 2**: 10 × 5 mm = 10,000 × 5,000 µm ✓
- [ ] **PZT thickness Phase 1 → Phase 2**: 100 µm (specified in material stack) ✓
- [ ] **Electrode area Phase 0 → Phase 2**: 8 × 4 mm = 8000 × 4000 µm ✓

**Overall alignment**: [ ] PASS (no discrepancies) [ ] MINOR (documented below) [ ] MAJOR (STOP)

Discrepancies (if any):
- ________________________________________________________________
- ________________________________________________________________

---

## Section 5: Fabrication Data Package

### Required Documents
1. [ ] **GDS-II files** (3 masks):
   - [ ] mask_1_body_outline.gds (signature: ____________________)
   - [ ] mask_2_electrodes.gds (signature: ____________________)
   - [ ] mask_3_release_slots.gds (signature: ____________________)

2. [ ] **Layer definition map** (`layer_map.txt` or PDF):
   - Layer assignments, purposes, feature descriptions
   - File hash (MD5 or SHA256): __________________________

3. [ ] **Process traveler** (`phase2/mems_process_traveler.md`):
   - 14 process steps with parameters, tolerances, QA checkpoints
   - File hash: __________________________

4. [ ] **Design rules document** (`phase2/design_rules.md`):
   - 20+ detailed design rules with rationale
   - File hash: __________________________

5. [ ] **DRC report** (`design/mems_layout/drc_report.json`):
   - Automated design rule check results
   - File hash: __________________________

6. [ ] **Test structure list** (`test_structures.txt`):
   - Probe site coordinates for parametric testing
   - Expected at least 4 sites (corners of reticle): [ ] Defined [ ] TBD

7. [ ] **Contact information**:
   - **Project Manager**: _________________________ | Phone: _____________ | Email: _____________
   - **Technical Lead**: _________________________ | Phone: _____________ | Email: _____________
   - **Emergency contact**: _________________________ | Phone: _____________ | Email: _____________

### Data Integrity
- [ ] **All files digitally signed** (GPG or S/MIME, if required by foundry)
- [ ] **Checksum manifest** created (list of file hashes)
- [ ] **Backup copy** stored locally (offline or cloud)
- [ ] **Archive format**: .zip with clear directory structure

---

## Section 6: Foundry Selection & Contracting

### Foundry Options & Timeline

| Foundry | Lead Time | Cost/Wafer | Notes | Selected |
|---|---|---|---|---|
| **SiNE (Singapore)** | 10 weeks | $8–12K | Excellent DRIE, PZT bonding | [ ] |
| **OA Xiamen (China)** | 8 weeks | $5–8K | Good yield, lower cost | [ ] |
| **IMEC (Belgium)** | 12 weeks | $15–20K | Premium process, R&D rates | [ ] |

- [ ] **Selected foundry**: _________________________ | Contact: ________________________
- [ ] **Project code assigned**: _________________________ | Run number: _________
- [ ] **MPW shuttle deadline**: _________________________ (date)
- [ ] **Minimum order quantity (MOQ)**: _________ die (typically 100–500 for 1/4 wafer)
- [ ] **Total quantity ordered**: _________ die

### Cost Estimate Breakdown
- [ ] **Mask set cost**: $ _______________ (3 masks × $1,000–$3,000 each)
- [ ] **Wafer run cost**: $ _______________ (includes processing, dicing, QA)
- [ ] **Packaging (optional)**: $ _______________
- [ ] **Shipping & expedite (if any)**: $ _______________
- **Total project cost**: $ _______________

### Foundry Contract & NDA
- [ ] **Foundry NDA signed**: Date: _________ | Parties: _____________________
- [ ] **Process agreement executed**: Date: _________
- [ ] **IP protection clause**: Reviewed and accepted
- [ ] **Confidentiality terms**: 5 years (typical)

---

## Section 7: Pre-Submission Sanity Checks

### Final Verification Checklist
- [ ] All 3 GDS-II masks generated and validated
- [ ] DRC PASS status (or documented waivers)
- [ ] Layer map and design rules documented
- [ ] Process traveler reviewed and approved
- [ ] Cross-checks with Phase 0/Phase 1 completed
- [ ] 2× independent design review sign-offs obtained
- [ ] Foundry selected and project code assigned
- [ ] Mask specifications defined and quoted
- [ ] Test structure list defined (probe sites, parametric tests)
- [ ] Complete data package assembled (.zip archive)
- [ ] Backup copy archived (local or cloud)
- [ ] Cost estimate and timeline communicated to stakeholders
- [ ] Funding approved for mask set ($3K–$8K) and wafer run ($5K–$15K)

### Risk Assessment
**Technical risks**:
- [ ] DRIE depth tolerance ±20 µm acceptable (cavity = 400 ± 20 µm)?  Yes [ ] No [ ]
- [ ] PZT epoxy bonding yield >95%?  Yes [ ] No [ ]
- [ ] HF vapor release reliable (45 ± 5 min etch time)?  Yes [ ] No [ ]
- [ ] Hinge deflection within spec (<100 µm @ 10 mN)?  Yes [ ] No [ ]

**Schedule risks**:
- [ ] Mask production on schedule (+1–2 weeks buffer)?  Yes [ ] No [ ]
- [ ] Foundry capacity available on target date?  Yes [ ] No [ ]
- [ ] Assembly/packaging planned for post-fab (Phase 3)?  Yes [ ] No [ ]

**Cost risks**:
- [ ] Budget approved for total project cost?  Yes [ ] No [ ]
- [ ] Contingency allocated (typically +20%)?  Yes [ ] No [ ]

**Mitigation plans** (if any "No" answers above):
- ________________________________________________________________
- ________________________________________________________________

---

## Section 8: Post-Submission Steps

### Timeline After Submission
- **Week 1**: Foundry reviews data package, requests clarifications (if any)
- **Week 2–3**: Masks manufactured at photomask vendor
- **Week 4**: Mask delivery to foundry + final inspection
- **Week 5–10**: Wafer processing (14-step process traveler)
- **Week 11**: Wafer dicing and die packaging
- **Week 12**: Yield analysis + die shipment to project

### Deliverables to Expect
- [ ] **Mask receipt confirmation** (scan of masks + Certificate of Conformance)
- [ ] **In-process inspection reports** (SEM images, profilometer depth scans)
- [ ] **Yield summary report** (% die passing continuity test)
- [ ] **Die samples** (10–20 units for preliminary testing)
- [ ] **Complete wafer lot** (100+ die, packaged in trays)
- [ ] **Process data package** (all SEM images, thickness measurements, test results)

### Next Phase (Phase 2B: Assembly & Testing)
- [ ] Plan die packaging (leadframe, wire bonding, epoxy glob)
- [ ] Plan initial functional test (electrical continuity, hinge deflection)
- [ ] Plan wind tunnel characterization (Phase 1 test protocol adapted for MEMS)

---

**Checklist Version**: Phase 2 v1.0 (2026-04-03)  
**Last Updated**: ___________________________ (date)  
**Approval**: [  ] Ready for foundry submission [  ] Needs revision [  ] On hold

**Signature**:  
Project Lead: _________________________ Date: _________  
Foundry Contact: _________________________ Date: _________
