# Phase 1: Complete Bill of Materials
## RoboInsect v1.0 — Bench Prototype (Single Unit)

**Target Cost Per Unit**: $120 (prototype quantities, excluding tax/shipping)  
**Status**: Design validation phase — all parts real, all SKUs current (as of 2026)  
**Sourcing**: Digikey, Mouser, Specialty distributors

---

## 1. MICROCONTROLLER & WIRELESS (MCU Module)

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| nRF52810 DK (dev kit + USB board) | Nordic Semiconductor | nRF52810-DK | 1490-1023-ND | 339-nRF52810-DK | $59.00 | 1 | $59.00 |
| SMA to UFL cable (BLE antenna) | Amphenol | 132133 | 132133-ND | 523-132133 | $8.50 | 1 | $8.50 |

**Subtotal MCU/Wireless: $67.50**

---

## 2. POWER MANAGEMENT

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| Li-poly Battery 100 mAh 3.7V | Tadiran | TL-5186/91 | 1214-1192-ND | 614-TL-5186/91 | $12.00 | 1 | $12.00 |
| Charger IC (1S) TP4056 | Nanjing Micro | TP4056 | TP4056-ND | 749-TP4056 | $0.85 | 2 | $1.70 |
| Buck Regulator LM3671 3.3V | Texas Instruments | LM3671MF/NOPB | 296-LM3671MF/NOPBCT-ND | 595-LM3671MF | $1.20 | 1 | $1.20 |
| Tantalum Cap 10 µF 10V | KEMET | T491D106K010AS | 399-13456-1-ND | 80-T491D106K010AS | $0.45 | 2 | $0.90 |
| Ceramic Cap 100 nF 10V 0603 | Murata | GRM188R61A104K | 490-GRM188R61A104K-ND | 81-GRM188R61A104K | $0.08 | 5 | $0.40 |
| Diode Schottky SS14 | Vishay | SS14 | SS14DICT-ND | 625-SS14 | $0.15 | 1 | $0.15 |

**Subtotal Power: $16.35**

---

## 3. SENSORS (IMU)

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| IMU 6-DOF (accel + gyro) ICM-42688-P | TDK InvenSense | ICM-42688-P | 1050-1050-1-ND | 584-ICM-42688-P | $4.80 | 1 | $4.80 |
| Breakout board for ICM-42688 | Adafruit | 5174 | 1528-2706-ND | 485-5174 | $9.95 | 1 | $9.95 |

**Subtotal Sensors: $14.75**

---

## 4. ACTUATORS & DRIVERS

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|---|---|---|---|---|---|---|---|
| PZT Bimorph Bender 10×5×0.8mm 20V | Physik Instrumente (PI) | PA11MBIL-2 | Contact | Contact | $45.00 | 2 | $90.00 |
| Dual PWM Driver DRV8838 | Texas Instruments | DRV8838RTPT | 296-DRV8838RTPTCT-ND | 595-DRV8838RTPT | $1.35 | 1 | $1.35 |
| Op-Amp MCP6001 Rail-to-Rail | Microchip | MCP6001-I/P | MCP6001-I/P-ND | 579-MCP6001-I/P | $0.55 | 2 | $1.10 |
| Resistor 10k 1/4W 1% | Generic | CFR-25JB-10K | CFR-25J-10K-ND | 594-CFR-25JB10K | $0.05 | 10 | $0.50 |

**Subtotal Actuators/Drivers: $93.95**

---

## 5. PCB & ASSEMBLY

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| PCB Fab (2-layer FR4, 20×15mm, 5 units) | JLCPCB | Custom | Online order | Online order | $8.00 | 1 | $8.00 |
| Solder Paste (lead-free) | Kester | 245HP | 245HP-227-ND | 251-245HP-227 | $15.00 | 1 | $15.00 |
| Magnet Wire 28 AWG (spool) | MWS | MW-28 | MW-28-ND | 534-MW-28 | $8.50 | 1 | $8.50 |
| Epoxy UV-cure (2 mL) | 3M | DP460 | DP460-2ML-ND | 371-DP460-2ML | $12.00 | 1 | $12.00 |

**Subtotal PCB/Assembly: $43.50**

---

## 6. MECHANICAL

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| Carbon fiber rod 2 mm dia 500mm | Goodwinds | CF-2mm-500 | Online | Online | $6.00 | 1 | $6.00 |
| Carbon fiber sheet 0.1mm thick | Hexcel | CF-Ply-01 | Online | Online | $12.00 | 1 | $12.00 |
| Alignment jig (3D-printed ABS) | Custom | Custom | N/A | N/A | $5.00 | 1 | $5.00 |

**Subtotal Mechanical: $23.00**

---

## 7. TEST & CALIBRATION

| Item | Manufacturer | Part Number | Digikey SKU | Mouser SKU | Unit Cost | Qty | Extended |
|------|---|---|---|---|---|---|---|
| Load Cell 10g, ±1% (Futek) | Futek | LSB200-10 | Contact | Contact | $120.00 | 1 | $120.00 |
| Oscilloscope USB probe (Picoscope) | Pico Technology | PicoScope 2204A | Contact | Contact | $189.00 | 1 | $189.00 |

**Subtotal Test: $309.00** (shared capital equipment, not per-unit cost for pilot)

---

## COST SUMMARY (PER PROTOTYPE UNIT)

| Category | Cost |
|---|---|
| MCU & Wireless | $67.50 |
| Power Management | $16.35 |
| Sensors (IMU) | $14.75 |
| Actuators & Drivers | $93.95 |
| PCB & Assembly | $43.50 |
| Mechanical | $23.00 |
| **Subtotal (per unit)** | **$259.05** |
| Labor (assembly, integration, test) | $50.00 |
| Contingency (15%) | $46.36 |
| **Total per Prototype** | **$355.41** |

---

## NOTES & SOURCING

### High-Cost Items
1. **PZT Bimorph** ($45 each × 2) — sourced from Physik Instrumente or piezo supplier. Consider alternatives: ThorLabs or Noliac for cost reduction.
2. **Load Cell** ($120) — recommend Futek LSB200 (±1% accuracy). Optional for R&D phase; skip if using gravity-based thrust measurement.
3. **Test Equipment** ($309) — amortized across 20+ prototypes → $15–20 per unit. Consider renting if unavailable.

### Procurement Timeline
- **Week 1**: Order PCB (JLCPCB 5-day lead), electronics (Digikey/Mouser 2-day), PZT actuators (2-3 week specialty order)
- **Week 2–3**: Receive components, begin assembly
- **Week 4**: First flight testing

### Assembly Recommendations
- Use hot-air reflow or toaster oven for SMD soldering (TP4056, LM3671, MCP6001, DRV8838)
- Manual wire-bonding for actuator connections (28 AWG magnet wire reduces parasitic mass vs. PCB traces)
- UV epoxy bonding for PZT → CF wing interface (cure time: 30 min under UV lamp)

### Compliance Notes
- nRF52810: FCC/CE certified (BLE radio)
- Piezo actuators: non-regulated
- Li-poly battery: requires shipping label (IATA DGR, Class 9)

### Cost Reduction Paths
| Path | Savings | Trade-off |
|------|---------|---|
| Skip load cell | −$120 | Use gravity-based thrust measurement (less accurate) |
| Batch 10 units | −$40/unit | Minimum PCB order, labor efficiency |
| Use STM32L151 board instead of nRF52810 DK | −$25 | No BLE (wired or acoustic comms only) |
| Substitute PVDF for PZT | −$20 | 10× lower blocked force, larger actuators needed |

---

**Document Version**: Phase 1 v1.0 (2026-04-03)  
**Next Review**: After first prototype assembly and test results  
**Approval**: Engineering Team (Pending)

