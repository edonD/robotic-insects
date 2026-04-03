# Module 02: Wing Aerodynamics — Requirements

## Questions to Answer

1. **Wing Geometry**: Wing span, wing area, airfoil shape
2. **Aerodynamic Coefficients**: Lift, drag, torque vs. angle of attack
3. **Thrust & Efficiency**: Power required vs. force produced
4. **Control Margins**: Authority to pitch, roll, yaw

## Inputs

- From Module 00: Wing beat frequency, stroke amplitude, control requirements
- From Module 01: Actuator force available
- Literature: Dickinson et al. aerodynamic database, XFOIL polars

## Outputs

- Thrust vs. wing angle (mN)
- Drag coefficient (dimensionless)
- Control torque authority (mN·mm)
- Power budget (mW)

## Success Criteria

- Thrust-to-weight ratio ≥ 1.5 (margin for control & maneuvering)
- Drag < 50% of thrust
- Control authority > 20% of body mass × g
