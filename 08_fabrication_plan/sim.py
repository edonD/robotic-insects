#!/usr/bin/env python3
"""
Module 08: Fabrication Plan & Cost Analysis
============================================

Models:
  - Process yield (defect density model)
  - Cost per unit (materials, labor, overhead)
  - Cycle time estimates
  - Assembly and test procedures
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from util import save_results_json

# ============================================================================
# FABRICATION PARAMETERS
# ============================================================================

# PCB specifications
PCB_SIZE_MM2 = 100  # ~10mm x 10mm
PCB_LAYERS = 2

# Component counts
NUM_COMPONENTS = 15
NUM_MECHANICAL_PARTS = 20

# Manufacturing volumes
PROTOTYPE_BATCH_SIZE = 10
PRODUCTION_BATCH_SIZE = 100

# Yield model parameters
DEFECT_DENSITY_PER_MM2 = 0.01  # Defects per mm²
ASSEMBLY_ERROR_RATE = 0.02  # 2% chance of assembly failure

# Cost model (USD)
PCB_COST_PER_UNIT = 10.0
COMPONENT_COST_PER_UNIT = 25.0
MECHANICAL_COST_PER_UNIT = 5.0
LABOR_COST_PER_UNIT = 15.0
TEST_COST_PER_UNIT = 5.0
PACKAGING_COST_PER_UNIT = 2.0
OVERHEAD_MULTIPLIER = 1.2  # 20% overhead

# ============================================================================
# YIELD CALCULATION
# ============================================================================

def calculate_yield(pcb_size_mm2, num_components, assembly_error_rate):
    """
    Calculate manufacturing yield (fraction of good parts).

    Assumes independent failures:
    - PCB defect probability = 1 - exp(-defect_density * area)
    - Component placement errors = assembly_error_rate
    """
    # PCB yield (Poisson model)
    lambda_defects = DEFECT_DENSITY_PER_MM2 * pcb_size_mm2
    pcb_yield = np.exp(-lambda_defects)

    # Assembly yield (all components must be placed correctly)
    assembly_yield = (1 - assembly_error_rate) ** num_components

    # Overall yield
    total_yield = pcb_yield * assembly_yield

    return pcb_yield, assembly_yield, total_yield


# ============================================================================
# COST CALCULATION
# ============================================================================

def calculate_cost_per_unit(batch_size):
    """
    Calculate cost per unit including labor and overhead.

    Batch size affects labor costs (economies of scale).
    """
    # Base material costs
    pcb_cost = PCB_COST_PER_UNIT
    component_cost = COMPONENT_COST_PER_UNIT
    mechanical_cost = MECHANICAL_COST_PER_UNIT

    # Labor cost scales inversely with batch size
    labor_scaling = 1.0 / np.sqrt(max(batch_size, 1))
    labor_cost = LABOR_COST_PER_UNIT * labor_scaling

    # Test cost (fixed per unit)
    test_cost = TEST_COST_PER_UNIT

    # Packaging
    packaging_cost = PACKAGING_COST_PER_UNIT

    # Subtotal before overhead
    subtotal = (pcb_cost + component_cost + mechanical_cost +
                labor_cost + test_cost + packaging_cost)

    # Apply overhead
    total_cost = subtotal * OVERHEAD_MULTIPLIER

    return {
        'material': pcb_cost + component_cost + mechanical_cost,
        'labor': labor_cost,
        'test': test_cost,
        'packaging': packaging_cost,
        'subtotal': subtotal,
        'overhead': subtotal * (OVERHEAD_MULTIPLIER - 1),
        'total': total_cost
    }


# ============================================================================
# CYCLE TIME CALCULATION
# ============================================================================

def calculate_cycle_time(batch_size):
    """
    Estimate cycle time (hours per unit) for small-batch manufacturing.

    Includes setup, assembly, test, and quality check.
    """
    # Setup time (amortized)
    setup_time_hours = 2.0
    setup_per_unit = setup_time_hours / batch_size

    # Assembly time (30 minutes per PCB)
    assembly_time = 0.5

    # Inspection time (10 minutes)
    inspection_time = 0.167

    # Test time (15 minutes)
    test_time = 0.25

    # Total per unit
    total_cycle_time = setup_per_unit + assembly_time + inspection_time + test_time

    return total_cycle_time


# ============================================================================
# MAIN SIMULATION
# ============================================================================

def main():
    print("=" * 70)
    print("WAVE 3: Fabrication Plan & Cost Analysis (Module 08)")
    print("=" * 70)
    print()

    print("1. YIELD ANALYSIS")
    print("-" * 70)

    pcb_yield, assembly_yield, total_yield = calculate_yield(
        PCB_SIZE_MM2, NUM_COMPONENTS, ASSEMBLY_ERROR_RATE
    )

    print(f"PCB defect density: {DEFECT_DENSITY_PER_MM2} per mm²")
    print(f"PCB area: {PCB_SIZE_MM2} mm²")
    print(f"Expected PCB defects per unit: {DEFECT_DENSITY_PER_MM2 * PCB_SIZE_MM2:.2f}")
    print(f"PCB yield: {pcb_yield*100:.1f}%")
    print()
    print(f"Component count: {NUM_COMPONENTS}")
    print(f"Assembly error rate: {ASSEMBLY_ERROR_RATE*100:.1f}%")
    print(f"Assembly yield: {assembly_yield*100:.1f}%")
    print()
    print(f"Overall manufacturing yield: {total_yield*100:.1f}%")
    print()

    print("2. COST ANALYSIS")
    print("-" * 70)

    # Prototype batch cost
    proto_cost = calculate_cost_per_unit(PROTOTYPE_BATCH_SIZE)
    proto_total_with_yield = proto_cost['total'] / total_yield  # Amortize failed units

    # Production batch cost
    prod_cost = calculate_cost_per_unit(PRODUCTION_BATCH_SIZE)
    prod_total_with_yield = prod_cost['total'] / total_yield

    print(f"Prototype batch size: {PROTOTYPE_BATCH_SIZE}")
    print(f"  Cost per unit (successful): ${proto_cost['total']:.2f}")
    print(f"  Cost per unit (accounting for yield): ${proto_total_with_yield:.2f}")
    print()
    print(f"Production batch size: {PRODUCTION_BATCH_SIZE}")
    print(f"  Cost per unit (successful): ${prod_cost['total']:.2f}")
    print(f"  Cost per unit (accounting for yield): ${prod_total_with_yield:.2f}")
    print()

    print("3. CYCLE TIME ANALYSIS")
    print("-" * 70)

    proto_cycle = calculate_cycle_time(PROTOTYPE_BATCH_SIZE)
    prod_cycle = calculate_cycle_time(PRODUCTION_BATCH_SIZE)

    print(f"Prototype batch cycle time per unit: {proto_cycle:.2f} hours")
    print(f"Prototype batch total time: {proto_cycle * PROTOTYPE_BATCH_SIZE:.1f} hours")
    print()
    print(f"Production batch cycle time per unit: {prod_cycle:.2f} hours")
    print(f"Production batch total time: {prod_cycle * PRODUCTION_BATCH_SIZE:.1f} hours")
    print()

    # Plotting
    print("4. GENERATING PLOTS...")

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Plot 1: Yield vs. batch size
    ax = axes[0, 0]
    batch_sizes = np.array([5, 10, 20, 50, 100, 200])
    # Yield is independent of batch size in this model
    yields = [total_yield * 100] * len(batch_sizes)
    ax.axhline(total_yield*100, color='b', linestyle='-', linewidth=2.5, label=f'Overall: {total_yield*100:.1f}%')
    ax.axhline(assembly_yield*100, color='g', linestyle='--', linewidth=2, label=f'Assembly: {assembly_yield*100:.1f}%')
    ax.axhline(pcb_yield*100, color='r', linestyle='--', linewidth=2, label=f'PCB: {pcb_yield*100:.1f}%')
    ax.set_xlabel('Batch Size', fontsize=11)
    ax.set_ylabel('Yield (%)', fontsize=11)
    ax.set_title('Manufacturing Yield', fontweight='bold')
    ax.set_ylim([0, 100])
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Plot 2: Cost per unit vs. batch size
    ax = axes[0, 1]
    costs_proto = []
    costs_prod = []
    for bs in batch_sizes:
        cost_breakdown = calculate_cost_per_unit(bs)
        costs_proto.append(cost_breakdown['total'])
        costs_prod.append(cost_breakdown['total'] / total_yield)

    ax.plot(batch_sizes, costs_proto, 'b-o', linewidth=2.5, markersize=6, label='Successful units')
    ax.plot(batch_sizes, costs_prod, 'r--s', linewidth=2.5, markersize=6, label='Accounting for yield')
    ax.set_xlabel('Batch Size', fontsize=11)
    ax.set_ylabel('Cost per Unit (USD)', fontsize=11)
    ax.set_title('Manufacturing Cost Analysis', fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3, which='both')
    ax.legend()

    # Plot 3: Cost breakdown (prototype)
    ax = axes[1, 0]
    categories = ['Material', 'Labor', 'Test', 'Packaging', 'Overhead']
    values = [proto_cost['material'], proto_cost['labor'], proto_cost['test'],
              proto_cost['packaging'], proto_cost['overhead']]
    colors_breakdown = ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728', '#9467bd']
    ax.pie(values, labels=categories, autopct='%1.1f%%', colors=colors_breakdown, startangle=90)
    ax.set_title(f'Cost Breakdown (Prototype, ${proto_cost["total"]:.2f})', fontweight='bold')

    # Plot 4: Cycle time
    ax = axes[1, 1]
    labels = ['Prototype\n(batch 10)', 'Production\n(batch 100)']
    cycle_times = [proto_cycle, prod_cycle]
    total_times = [proto_cycle * PROTOTYPE_BATCH_SIZE, prod_cycle * PRODUCTION_BATCH_SIZE]
    colors_cycle = ['#ff7f0e', '#2ca02c']

    x_pos = np.arange(len(labels))
    ax.bar(x_pos - 0.2, cycle_times, 0.4, label='Per unit (hours)', color=colors_cycle)
    ax.bar(x_pos + 0.2, np.array(total_times)/10, 0.4, label='Batch total (hours / 10)', color=['#1f77b4', '#d62728'])

    ax.set_ylabel('Time (hours)', fontsize=11)
    ax.set_title('Cycle Time Analysis', fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('08_fabrication_plan/fabrication_analysis.png', dpi=150, bbox_inches='tight')
    print(f"   OK: Saved: 08_fabrication_plan/fabrication_analysis.png")
    print()

    # Save results
    print("5. WRITING RESULTS...")
    with open('08_fabrication_plan/results.md', 'w', encoding='utf-8') as f:
        f.write("# Fabrication Plan & Cost Analysis — Results\n\n")
        f.write("**Model**: Yield model, cost breakdown, cycle time estimation\n\n")
        f.write("## Manufacturing Yield\n\n")
        f.write(f"- **PCB yield**: {pcb_yield*100:.1f}%\n")
        f.write(f"- **Assembly yield**: {assembly_yield*100:.1f}%\n")
        f.write(f"- **Overall yield**: {total_yield*100:.1f}%\n\n")
        f.write("## Cost per Unit\n\n")
        f.write(f"- **Prototype batch (n={PROTOTYPE_BATCH_SIZE})**: ${proto_cost['total']:.2f} (successful), ${proto_total_with_yield:.2f} (w/ yield)\n")
        f.write(f"- **Production batch (n={PRODUCTION_BATCH_SIZE})**: ${prod_cost['total']:.2f} (successful), ${prod_total_with_yield:.2f} (w/ yield)\n\n")
        f.write("## Cost Breakdown (Prototype)\n\n")
        f.write(f"- **Material**: ${proto_cost['material']:.2f} ({proto_cost['material']/proto_cost['subtotal']*100:.1f}%)\n")
        f.write(f"- **Labor**: ${proto_cost['labor']:.2f} ({proto_cost['labor']/proto_cost['subtotal']*100:.1f}%)\n")
        f.write(f"- **Test**: ${proto_cost['test']:.2f} ({proto_cost['test']/proto_cost['subtotal']*100:.1f}%)\n")
        f.write(f"- **Packaging**: ${proto_cost['packaging']:.2f} ({proto_cost['packaging']/proto_cost['subtotal']*100:.1f}%)\n\n")
        f.write("## Cycle Time\n\n")
        f.write(f"- **Per unit (prototype)**: {proto_cycle:.2f} hours\n")
        f.write(f"- **Per unit (production)**: {prod_cycle:.2f} hours\n\n")
        f.write("## Evaluation Status\n\n")
        f.write("Awaiting evaluator.py...\n")

    print(f"   OK: Saved: 08_fabrication_plan/results.md")
    print()

    # Save JSON results
    results = {
        'pcb_yield_percent': float(pcb_yield * 100),
        'assembly_yield_percent': float(assembly_yield * 100),
        'overall_yield_percent': float(total_yield * 100),
        'prototype_cost_per_unit_usd': float(proto_cost['total']),
        'prototype_cost_with_yield_usd': float(proto_total_with_yield),
        'production_cost_per_unit_usd': float(prod_cost['total']),
        'production_cost_with_yield_usd': float(prod_total_with_yield),
        'prototype_cycle_time_hours': float(proto_cycle),
        'production_cycle_time_hours': float(prod_cycle),
    }
    save_results_json('08_fabrication_plan', results)

    print("=" * 70)
    print("DONE. Fabrication plan analysis complete. Run evaluator.py to grade.")
    print("=" * 70)


if __name__ == '__main__':
    main()
