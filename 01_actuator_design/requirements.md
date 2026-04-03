# Module 01: Actuator Design — Requirements

## Questions to Answer

1. **Actuator Selection**
   - Piezoelectric (fast, lightweight, low force) or Shape-Memory Alloy (high force, lower bandwidth)?
   - What material? (PZT, PVDF, Nitinol)

2. **Force & Displacement**
   - How much force is needed to move the wing (from Module 00)?
   - How much stroke displacement (mm) is needed?

3. **Frequency Response**
   - Can the actuator follow the 100–200 Hz wing beat?
   - What is the actuator resonance frequency?

4. **Power Consumption**
   - How much electrical power does the actuator draw?
   - Is this compatible with battery/wireless power budget?

5. **Scaling & Miniaturization**
   - How small can the actuator be made?
   - What are manufacturing limits?

---

## Input Data

**From Module 00:**
- Peak muscle force required
- Wing beat frequency
- Control bandwidth

**From literature:**
- MIT RoboBees papers: Piezo actuator scaling laws
- Paez et al.: Micro SMA actuators

---

## Outputs

- `results.md`: Actuator type, force rating, displacement, resonance frequency, power consumption, mass
- Plots: Force vs. frequency, power vs. displacement

---

## Success Criteria (Evaluator)

- Actuator force ≥ 1.5 × peak muscle force (design margin)
- Resonance frequency > 2 × wing beat frequency (avoid resonant damping)
- Power consumption < 50 mW (battery compatible)
- Fabrication complexity: MEMS-compatible (foundry producible)
