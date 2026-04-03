# Phase 1: PCB Schematic — RoboInsect v1.0 Control Board

**Board Size**: 20×15 mm FR4 2-layer  
**Connector Type**: 0.1" 2×5 header (J1) for nRF52 DK dock  
**Voltage Rails**: 3.3V (digital), 5V (charger input), GND

---

## POWER SECTION (Left Side)

```
        +BATT
         |
        [D1]  (SS14 Schottky diode)
         |
        [TP4056 Charger IC]
        |  |  |
       +5V - GND
         |
        [R_charge] (10k)
         |
        [C1] (10µ Tant)
         |
        GND

        +5V (from charger or USB)
         |
        [LM3671 3.3V Buck]
        |  |  |
       +3.3V - GND
         |
        [C2,C3] (100nF)
         |
        GND
```

---

## MICROCONTROLLER (Center — nRF52810 DK)

```
     [nRF52810 DK]
     |  |  |  |  |
    GND +3.3V
     SWD interface (reserved for programming)
     GPIO:
       P0.13 → PWM1 (Actuator 1 enable)
       P0.14 → PWM2 (Actuator 2 enable)
       P0.15 → DIR1  (Actuator 1 direction)
       P0.16 → DIR2  (Actuator 2 direction)
       P0.17 → SDA   (IMU I2C)
       P0.18 → SCL   (IMU I2C)
       P0.19 → AREF  (Load cell analog input, via op-amp)
       P0.20 → RX    (Serial debug @ 115200 baud)
       P0.21 → TX    (Serial debug)
```

---

## SENSOR SECTION (Right Top)

```
    [ICM-42688 Breakout]
     |  |  |  |  |
    GND +3.3V
     SDA → nRF52 P0.17
     SCL → nRF52 P0.18
     INT → P0.22 (interrupt, optional)
    
    [C4] 100nF bypass cap on +3.3V rail
```

---

## ACTUATOR DRIVER (Right Bottom)

```
     [DRV8838 PWM Driver] (Motor driver IC)
     |  |  |  |  |  |
    GND +3.3V
    
    IN1 ← nRF52 P0.13 (PWM frequency 1 kHz)
    IN2 ← nRF52 P0.15 (direction control)
    OUT1 → Actuator 1+
    OUT2 → Actuator 1-
    
    [Sense resistor] 0.22Ω (1/4W) between OUT2 and GND
    Voltage divider: sense → 10k/10k → nRF52 P0.19 (via MCP6001 op-amp)
    
    [C5] 100nF close to DRV8838 power pin
    [C6] 10µF tantalum on +3.3V rail

Second DRV8838 (for Actuator 2):
    IN1 ← nRF52 P0.14
    IN2 ← nRF52 P0.16
    OUT → Actuator 2
```

---

## SENSING CIRCUIT (Op-Amp)

```
    [MCP6001 Op-Amp] (for force/thrust measurement)
    
    Non-inverting (+): sense resistor voltage from actuator
    Inverting (-): voltage divider reference (1.65V = mid-rail)
    Output: → nRF52 P0.19 (ADC)
    
    Gain = 2 (10k/10k divider on feedback)
    
    [C7] 10nF feedback capacitor
    [C8] 100nF bypass on op-amp supply
```

---

## CONNECTOR J1 — DOCK TO nRF52810 DK

**Pin-out** (2×5 header, 0.1" spacing):

```
Row A (top):    GND   P0.13  P0.15  P0.17  P0.19
Row B (bottom): +3.3V P0.14  P0.16  P0.18  P0.20

(Connects to nRF52 DK via jumper wires or pogo pins)
```

---

## TEST PADS

**Located at board edges** for oscilloscope / voltmeter probing:

- TP1: +3.3V rail
- TP2: +5V (charger)
- TP3: GND
- TP4: Actuator 1 sense voltage
- TP5: Actuator 2 sense voltage
- TP6: nRF52 TX (serial debug)
- TP7: nRF52 RX (serial debug)

---

## SIGNAL INTEGRITY NOTES

1. **Power Distribution**:
   - Place 100nF bypass caps within 5mm of each IC power pin
   - 10µ tantalum capacitors on rails for bulk energy storage
   - Separate GND planes on L1 (top) and L2 (bottom)

2. **High-Speed Signals** (PWM @ 1 kHz, I2C @ 400 kHz):
   - Keep SDA/SCL runs short (<20 mm)
   - Add 4.7k pull-ups to +3.3V (I2C)
   - Route PWM traces away from analog sense nodes

3. **Analog Measurement** (Load cell signal < 10 mV):
   - Shield sense resistor with ground pour
   - Op-amp feedback loop in inner layer if possible
   - No switching noise sources near op-amp

4. **Thermal**:
   - DRV8838 can dissipate ~1W; add small copper pour (thermal via to backside if needed)
   - LM3671 regulator: low current (<200 mA), no heatsink needed

---

## BILL OF MATERIALS (for PCB Assembly)

| Reference | Part | Value | Qty |
|---|---|---|---|
| D1 | Schottky Diode | SS14 | 1 |
| C1, C2, C3, C5, C8 | Ceramic Cap | 100nF 0603 | 5 |
| C4, C6, C7 | Capacitor | 10µ Tant / 10nF Cer | 3 |
| R_sense | Resistor | 0.22Ω 1/4W | 2 |
| R_pullup | Resistor | 4.7k 1/4W | 2 |
| U1, U2 | DRV8838 | SOIC-8 | 2 |
| U3 | MCP6001 | DIP-8 or SOIC-8 | 1 |
| TP1-TP7 | Test Pad | - | 7 |
| J1 | Header | 2×5 0.1" | 1 |
| External | nRF52810 DK | Dev board | 1 |
| External | ICM-42688 Breakout | - | 1 |

---

**Schematic Version**: v1.0 (2026-04-03)  
**EDA Tool**: KiCad 6.0+ (Gerber files for JLCPCB)  
**Design Approval**: Pending validation build

