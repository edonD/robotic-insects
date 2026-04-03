#!/usr/bin/env python3
"""
Module 07: Swarm Coordination & Multi-Agent Behavior
====================================================

Implements:
  - Boids flocking algorithm (separation, alignment, cohesion)
  - Range-limited wireless communication
  - Collision avoidance with distance thresholds
  - Formation quality metrics
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import save_results_json

# ============================================================================
# SWARM PARAMETERS
# ============================================================================

NUM_ROBOTS = 6
ARENA_SIZE_M = 2.0
COMMUNICATION_RANGE_M = 0.5
COLLISION_DISTANCE_M = 0.1
SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.0

# ============================================================================
# CLASS: Robot Agent
# ============================================================================

class RobotAgent:
    """Individual robot in swarm."""

    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update_position(self, dt=0.01):
        """Update position based on velocity."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Boundary conditions (wraparound)
        self.x = self.x % ARENA_SIZE_M
        self.y = self.y % ARENA_SIZE_M

    def distance_to(self, other):
        """Euclidean distance to another robot."""
        dx = self.x - other.x
        dy = self.y - other.y
        return np.sqrt(dx**2 + dy**2)


# ============================================================================
# CLASS: Swarm Simulator
# ============================================================================

class SwarmSimulator:
    """Multi-agent swarm simulation using Boids algorithm."""

    def __init__(self, num_robots, arena_size_m):
        self.num_robots = num_robots
        self.arena_size = arena_size_m
        self.robots = []
        self.collision_count = 0
        self.time_step = 0

        # Initialize robots in random positions
        np.random.seed(42)
        for i in range(num_robots):
            x = np.random.rand() * arena_size_m
            y = np.random.rand() * arena_size_m
            vx = np.random.randn() * 0.1
            vy = np.random.randn() * 0.1
            self.robots.append(RobotAgent(x, y, vx, vy))

    def separation(self, robot):
        """Separation rule: avoid crowding neighbors."""
        steer = np.array([0.0, 0.0])
        count = 0

        for other in self.robots:
            d = robot.distance_to(other)
            if 0 < d < COMMUNICATION_RANGE_M:
                # Vector pointing away from neighbor
                dx = robot.x - other.x
                dy = robot.y - other.y
                mag = np.sqrt(dx**2 + dy**2)
                if mag > 0:
                    steer += np.array([dx/mag, dy/mag])
                    count += 1

        if count > 0:
            steer /= count

        return steer

    def alignment(self, robot):
        """Alignment rule: match velocity with neighbors."""
        avg_vel = np.array([0.0, 0.0])
        count = 0

        for other in self.robots:
            d = robot.distance_to(other)
            if 0 < d < COMMUNICATION_RANGE_M:
                avg_vel += np.array([other.vx, other.vy])
                count += 1

        if count > 0:
            avg_vel /= count
            avg_vel = avg_vel / (np.linalg.norm(avg_vel) + 1e-6)

        return avg_vel

    def cohesion(self, robot):
        """Cohesion rule: steer towards average location of neighbors."""
        center = np.array([0.0, 0.0])
        count = 0

        for other in self.robots:
            d = robot.distance_to(other)
            if 0 < d < COMMUNICATION_RANGE_M:
                center += np.array([other.x, other.y])
                count += 1

        if count > 0:
            center /= count
            # Steer towards center
            dx = center[0] - robot.x
            dy = center[1] - robot.y
            mag = np.sqrt(dx**2 + dy**2)
            if mag > 0:
                return np.array([dx/mag, dy/mag])

        return np.array([0.0, 0.0])

    def check_collisions(self):
        """Count pairwise collisions."""
        collisions = 0
        for i, robot_a in enumerate(self.robots):
            for robot_b in self.robots[i+1:]:
                if robot_a.distance_to(robot_b) < COLLISION_DISTANCE_M:
                    collisions += 1
        return collisions

    def update_step(self, dt=0.01):
        """Single simulation step."""
        # Update velocities based on Boids rules
        for robot in self.robots:
            sep = self.separation(robot)
            align = self.alignment(robot)
            coh = self.cohesion(robot)

            # Weighted combination
            acc = (SEPARATION_WEIGHT * sep +
                   ALIGNMENT_WEIGHT * align +
                   COHESION_WEIGHT * coh)

            # Update velocity (with max speed limit)
            robot.vx += acc[0] * dt
            robot.vy += acc[1] * dt

            max_speed = 0.5
            speed = np.sqrt(robot.vx**2 + robot.vy**2)
            if speed > max_speed:
                robot.vx *= max_speed / speed
                robot.vy *= max_speed / speed

            # Update position
            robot.update_position(dt)

        # Check collisions
        self.collision_count += self.check_collisions()
        self.time_step += 1

    def formation_quality(self):
        """Metric: average distance between robots (higher = spread out)."""
        if self.num_robots < 2:
            return 0.0

        total_dist = 0
        count = 0
        for i, robot_a in enumerate(self.robots):
            for robot_b in self.robots[i+1:]:
                total_dist += robot_a.distance_to(robot_b)
                count += 1

        return total_dist / count if count > 0 else 0.0


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 3: Swarm Coordination & Multi-Agent Behavior (Module 07)")
    print("=" * 70)
    print()

    print("1. SWARM INITIALIZATION")
    print("-" * 70)
    swarm = SwarmSimulator(NUM_ROBOTS, ARENA_SIZE_M)
    print(f"Number of robots: {NUM_ROBOTS}")
    print(f"Arena size: {ARENA_SIZE_M} x {ARENA_SIZE_M} m")
    print(f"Communication range: {COMMUNICATION_RANGE_M} m")
    print(f"Collision distance: {COLLISION_DISTANCE_M} m")
    print()

    print("2. RUNNING SWARM SIMULATION (200 timesteps)")
    print("-" * 70)

    positions_history = []
    quality_history = []

    for step in range(200):
        swarm.update_step(dt=0.01)

        if step % 20 == 0:
            quality = swarm.formation_quality()
            quality_history.append(quality)
            print(f"  Step {step:3d}: formation quality = {quality:.3f} m, collisions = {swarm.collision_count}")

        # Store positions for visualization
        if step % 10 == 0:
            positions = [(r.x, r.y) for r in swarm.robots]
            positions_history.append(positions)

    avg_collision_rate = swarm.collision_count / swarm.time_step if swarm.time_step > 0 else 0
    final_quality = swarm.formation_quality()

    print()
    print(f"Final formation quality: {final_quality:.3f} m")
    print(f"Total collisions: {swarm.collision_count}")
    print(f"Collision rate: {avg_collision_rate:.4f} collisions/step")
    print()

    # Plotting
    print("3. GENERATING PLOTS...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Final formation
    ax = axes[0, 0]
    final_pos = positions_history[-1]
    x_vals = [p[0] for p in final_pos]
    y_vals = [p[1] for p in final_pos]
    ax.scatter(x_vals, y_vals, s=100, c=range(NUM_ROBOTS), cmap='tab10', edgecolors='black', linewidth=1.5)

    # Draw communication range around each robot
    for x, y in final_pos:
        circle = plt.Circle((x, y), COMMUNICATION_RANGE_M, fill=False, linestyle='--', alpha=0.3)
        ax.add_patch(circle)

    ax.set_xlim([-0.1, ARENA_SIZE_M + 0.1])
    ax.set_ylim([-0.1, ARENA_SIZE_M + 0.1])
    ax.set_aspect('equal')
    ax.set_xlabel('X (m)', fontsize=11)
    ax.set_ylabel('Y (m)', fontsize=11)
    ax.set_title('Final Swarm Formation', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Plot 2: Formation quality over time
    ax = axes[0, 1]
    steps_quality = list(range(0, 200, 20))
    ax.plot(steps_quality, quality_history, 'b-o', linewidth=2.5, markersize=6)
    ax.set_xlabel('Simulation Step', fontsize=11)
    ax.set_ylabel('Formation Quality (m)', fontsize=11)
    ax.set_title('Average Inter-Robot Distance', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Plot 3: Trajectory trails
    ax = axes[1, 0]
    for robot_idx in range(min(3, NUM_ROBOTS)):
        x_traj = [pos[robot_idx][0] for pos in positions_history]
        y_traj = [pos[robot_idx][1] for pos in positions_history]
        ax.plot(x_traj, y_traj, 'o-', linewidth=1.5, markersize=3, label=f'Robot {robot_idx}')

    ax.set_xlim([-0.1, ARENA_SIZE_M + 0.1])
    ax.set_ylim([-0.1, ARENA_SIZE_M + 0.1])
    ax.set_aspect('equal')
    ax.set_xlabel('X (m)', fontsize=11)
    ax.set_ylabel('Y (m)', fontsize=11)
    ax.set_title('Robot Trajectories (first 3)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 4: Performance metrics
    ax = axes[1, 1]
    ax.axis('off')

    metrics_text = f"""
    SWARM PERFORMANCE METRICS

    Final formation quality: {final_quality:.3f} m

    Total collisions: {swarm.collision_count}

    Collision rate: {avg_collision_rate:.4f} /step

    Communication range: {COMMUNICATION_RANGE_M} m

    Separation distance: {COLLISION_DISTANCE_M} m

    Swarm size: {NUM_ROBOTS} robots
    """

    ax.text(0.1, 0.9, metrics_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('07_swarm_coordination/swarm_analysis.png', dpi=150, bbox_inches='tight')
    print(f"   OK: Saved: 07_swarm_coordination/swarm_analysis.png")
    print()

    # Save results markdown
    print("4. WRITING RESULTS...")
    with open('07_swarm_coordination/results.md', 'w', encoding='utf-8') as f:
        f.write("# Swarm Coordination — Results\n\n")
        f.write("**Model**: Boids flocking algorithm with collision avoidance\n\n")
        f.write("## Swarm Configuration\n\n")
        f.write(f"- **Swarm size**: {NUM_ROBOTS} robots\n")
        f.write(f"- **Arena**: {ARENA_SIZE_M} x {ARENA_SIZE_M} m\n")
        f.write(f"- **Communication range**: {COMMUNICATION_RANGE_M} m\n")
        f.write(f"- **Collision distance**: {COLLISION_DISTANCE_M} m\n\n")
        f.write("## Simulation Results\n\n")
        f.write(f"- **Final formation quality**: {final_quality:.3f} m (avg inter-robot distance)\n")
        f.write(f"- **Total collisions**: {swarm.collision_count}\n")
        f.write(f"- **Collision rate**: {avg_collision_rate:.4f} per step\n\n")
        f.write("## Boids Weights\n\n")
        f.write(f"- **Separation**: {SEPARATION_WEIGHT}\n")
        f.write(f"- **Alignment**: {ALIGNMENT_WEIGHT}\n")
        f.write(f"- **Cohesion**: {COHESION_WEIGHT}\n\n")
        f.write("## Evaluation Status\n\n")
        f.write("Awaiting evaluator.py...\n")

    print(f"   OK: Saved: 07_swarm_coordination/results.md")
    print()

    # Save JSON results
    results = {
        'swarm_size': int(NUM_ROBOTS),
        'arena_size_m': float(ARENA_SIZE_M),
        'communication_range_m': float(COMMUNICATION_RANGE_M),
        'collision_distance_m': float(COLLISION_DISTANCE_M),
        'final_formation_quality_m': float(final_quality),
        'total_collisions': int(swarm.collision_count),
        'collision_rate_per_step': float(avg_collision_rate),
        'separation_weight': float(SEPARATION_WEIGHT),
        'alignment_weight': float(ALIGNMENT_WEIGHT),
        'cohesion_weight': float(COHESION_WEIGHT),
    }
    save_results_json('07_swarm_coordination', results)

    print("=" * 70)
    print("DONE. Swarm simulation complete. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
