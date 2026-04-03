# Phase 1: Troubleshooting Guide — RoboInsect v1.0

**Quick Reference**: Common failures, symptoms, causes, and fixes  
**Priority**: Work through these in order of likelihood

---

## 1. POWER & STARTUP

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| No power-on (no LED) | Dead/reversed battery | Check battery voltage | Charge battery, verify polarity |
| USB charger not working | Bad charger cable | Test with known good cable | Replace cable |
| Unstable voltage on TP1 | LM3671 regulator off | Measure V_out at LM3671 pin 5 | Re-solder regulator, check cap C1 |
| +3.3V rail drops under load | Weak power supply or short | Measure current draw | Check for solder bridges near power pins |

---

## 2. COMMUNICATION & PROGRAMMING

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| Serial port not detected | nRF52 not responding | Try `openocd -f nrf52810.cfg` | Reflash bootloader, check SWD wires |
| Garbled serial output | Baud rate mismatch | Check console settings (115200 baud) | Confirm firmware serial config |
| No I2C response from IMU | I2C bus stuck | Measure SDA/SCL voltage: should be ~3.3V | Check pull-up resistors (4.7k), resolder IMU |

---

## 3. WING VIBRATION ISSUES

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| Wing doesn't vibrate at all | Actuator not bonded | Gently pull wing tip (should move) | Re-epoxy bimorph to wing, cure 24h |
| Wing vibrates but weak | Low drive voltage | Measure PWM output on TP4/TP5 | Check DRV8838 output (should swing 0–5V) |
| One wing vibrates, one doesn't | Actuator or driver fault | Swap driver output connections | If same wing fails, actuator is bad (replace) |
| Vibration feels rough/jerky | Asymmetric epoxy bond | Visual inspection under magnifier | Remove actuator, clean, re-epoxy |
| Resonance frequency wrong | Wing mass changed or delamination | Run frequency sweep (50–300 Hz) | Add/remove weight, or re-bond if delaminated |

---

## 4. LOAD CELL / THRUST MEASUREMENT

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| No thrust reading (0 g) | Bad sense resistor or op-amp | Measure voltage at TP4 (op-amp output) | Check 0.22Ω resistor for opens, resolder op-amp |
| Thrust reading drifts over time | Load cell zero offset | Zero load cell, measure ADC at rest | Store offset in firmware, auto-subtract |
| Thrust reading noise (jumps ±0.5g) | ADC input coupling or ground noise | Check capacitor C7 (10nF feedback cap) | Add ferrite bead on sense line, improve grounding |
| Negative thrust (unrealistic) | Polarity issue or bad calibration | Verify load cell wiring direction | Flip sense resistor polarity, recalibrate |

---

## 5. CONTROL & STABILITY

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| PWM signals present but no movement | Motor driver H-bridge issue | Measure both output pins (IN1 & IN2) | Check DRV8838 datasheet, verify logic levels |
| Erratic thrust spikes | Electrical noise from PWM | Measure signal with oscilloscope at TP4 | Add capacitor filter (10–100nF) on sense line |
| Control loop unstable (oscillation) | PID tuning issue | Check Kp, Ki, Kd gains in firmware | Reduce Kp (proportional gain) by 50%, retest |

---

## 6. THERMAL ISSUES

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| Motor driver warm to touch (>50°C) | Excessive current or short | Measure current during operation | Check for shorted actuator turns (replace) |
| Thermal shutdown (device resets) | Overcurrent protection triggered | Reduce PWM duty cycle, run again | Check actuator resistance with ohmmeter |

---

## 7. MECHANICAL ISSUES

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| Wing detaches from actuator | Epoxy bond failed | Gently pull wing | Carefully remove wing, re-epoxy (UV DP460), 24h cure |
| Wire connections corrode | Moisture + solder flux residue | Visual inspection | Clean with IPA + soft brush, apply protective coating |
| CoG balance is off | Mass imbalance from assembly | Balance on sharp point | Add tape weights to heavier side |

---

## 8. DATA LOGGING / TEST SCRIPT ISSUES

| Symptom | Likely Cause | Test | Fix |
|---------|---|---|---|
| Script hangs on `connect_serial()` | Serial port busy or wrong port | `ls /dev/tty*` (Linux) | Specify correct port: `--port /dev/ttyUSB0` |
| CSV file not saved | Path permissions or missing directory | Check `phase1/` directory exists | Create directory: `mkdir -p phase1` |
| Plots don't show thrust peaks | No frequency sweep data | Check CSV has >10 rows | Run `--sweep 50 300` option |

---

## 9. UNEXPECTED OBSERVATIONS

| Observation | Normal? | Action |
|---|---|---|
| Wing frequency slightly off resonance | Yes | Tune by adjusting wing weight or epoxy thickness |
| Different thrust for left vs. right wing | No | Check symmetry of epoxy bonds and bimorph centering |
| IMU shows vibration at 2× wing frequency | Maybe | Could be flutter or blade passing frequency — investigate if excessive |
| Thrust decreases over several hours | No | Could indicate battery voltage drop — charge battery |
| Temperature rises slowly over 10 min | Yes (expected) | Check it plateaus; if keeps rising, reduce current |

---

## SYSTEMATIC TROUBLESHOOTING FLOWCHART

```
Does device power up?
├─ No → Check battery, regulator, continuity
├─ Yes → Does serial port connect?
    ├─ No → Check nRF52 bootloader, SWD wires
    ├─ Yes → Can you read IMU?
        ├─ No → Check I2C, pull-ups, IMU solder
        ├─ Yes → Do wings vibrate?
            ├─ No → Check actuator epoxy bond, driver voltages
            ├─ Yes → Is thrust > 1 mN?
                ├─ No → Increase drive voltage (max 25V), check bond
                ├─ Yes → PASS — Ready for wind tunnel test
```

---

## BACKUP COMPONENTS (Keep on Hand)

For rapid troubleshooting/repair:
- 2× nRF52810 DK (dev board, $59 each)
- 2× DRV8838 driver IC ($1.35 each)
- 2× MCP6001 op-amp ($0.55 each)
- 3× PZT-5H bimorph benders ($45 each)
- Solder paste, flux, wire, epoxy

---

**Last Updated**: Phase 1 v1.0 (2026-04-03)  
**Contact**: For hardware support, refer to manufacturer datasheets (PI, TI, nRF5 SDK docs)

