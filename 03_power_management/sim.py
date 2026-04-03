#!/usr/bin/env python3
"""Module 03: Power Management Simulation"""

def main():
    print("WAVE 2: Power Management (Module 03)")
    print()

    # Power budget
    actuator_power = 20  # mW (from Module 01)
    controller_power = 5  # mW
    total_power = actuator_power + controller_power

    # Battery assumption: Li-poly 3.7V, 100 mAh = 0.37 Wh
    battery_capacity_wh = 0.37
    flight_time_minutes = (battery_capacity_wh * 1000 / total_power) * 60

    print(f"Actuator power: {actuator_power} mW")
    print(f"Controller power: {controller_power} mW")
    print(f"Total: {total_power} mW")
    print(f"Battery capacity: {battery_capacity_wh} Wh")
    print(f"Flight time: {flight_time_minutes:.1f} minutes")
    print()

    with open('03_power_management/results.md', 'w') as f:
        f.write("# Power Management — Results\n\n")
        f.write(f"- Total power: {total_power} mW\n")
        f.write(f"- Flight time: {flight_time_minutes:.1f} min\n")

if __name__ == '__main__':
    main()
