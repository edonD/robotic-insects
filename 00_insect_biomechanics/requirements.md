# Module 00: Insect Biomechanics — Requirements

## Questions to Answer

1. **Wing Kinematics**
   - What is the natural wing beat frequency of our target insect (Drosophila, bee, dragonfly)?
   - What are the wing stroke amplitude and twist angles?
   - How does wing motion change during hovering vs. forward flight?

2. **Muscle Activation**
   - How many wing muscles are needed? (Drosophila has ~8 indirect flight muscles)
   - What is the duty cycle (% of time muscle is active)?
   - What force does each muscle need to produce?

3. **Center of Gravity & Moment of Inertia**
   - Where is the CoG relative to wing root?
   - What is the body moment of inertia (needed for attitude control)?

4. **Control Authority**
   - How much can wing asymmetry provide roll/pitch torque?
   - What is the minimum control bandwidth (Hz) for stable flight?

---

## Input Data

**From literature** (read these papers):
- Dickinson et al. (2000). "Active wing kinematics decouple inertial power from aerodynamic power in the fruit fly, Drosophila." *J. Exp. Biol.* 203, 1679–1694.
- Fry et al. (2005). "Context-dependent flight behaviour in Drosophila." *Nature* 437, 1102–1105.
- Combes & Dudley (2002). "Turbulence-driven instabilities limit insect flight performance." *Nature* 412, 47–50.

**Enter into sim.py**:
- Target insect (e.g., "Drosophila melanogaster")
- Body mass (mg)
- Wing span (mm)
- Wing area (mm²)

---

## Outputs

- `results.md`: Wing beat frequency (Hz), duty cycle (%), muscle force (mN), CoG position (mm), control bandwidth (Hz)
- Plots: Wing trajectory, muscle activation, frequency response

---

## Success Criteria (Evaluator)

- Wing frequency matches literature (±5%)
- Muscle force is within biology range (1–50 mN for insects)
- CoG position is realistic (in thorax, not in wing)
- Control bandwidth > 20 Hz (needed for stable attitude control)
