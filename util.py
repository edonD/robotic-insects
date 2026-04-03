"""
Shared utilities for all simulation modules.

Provides:
- Path resolution (works from any working directory)
- JSON/Markdown result saving
- Numeric evaluator pattern
"""

from pathlib import Path
import json
import numpy as np

# Module directory (robotic-insects/)
REPO_ROOT = Path(__file__).parent

def get_module_path(module_name: str) -> Path:
    """
    Get the full path to a module directory.

    Args:
        module_name: e.g., "00_insect_biomechanics"

    Returns:
        Path object to the module directory
    """
    return REPO_ROOT / module_name

def save_results_json(module_name: str, data: dict):
    """
    Save results as JSON for numeric evaluation.

    Args:
        module_name: e.g., "00_insect_biomechanics"
        data: dict of results (will be JSON serializable)
    """
    module_path = get_module_path(module_name)
    results_file = module_path / "results.json"

    # Ensure all numpy types are converted to Python native types
    clean_data = {}
    for key, value in data.items():
        if isinstance(value, (np.ndarray, np.generic)):
            clean_data[key] = float(value) if np.isscalar(value) else value.tolist()
        else:
            clean_data[key] = value

    with open(results_file, 'w') as f:
        json.dump(clean_data, f, indent=2)

    return results_file

def load_results_json(module_name: str) -> dict:
    """
    Load results from JSON.

    Args:
        module_name: e.g., "00_insect_biomechanics"

    Returns:
        dict of results
    """
    module_path = get_module_path(module_name)
    results_file = module_path / "results.json"

    if not results_file.exists():
        return {}

    with open(results_file, 'r') as f:
        return json.load(f)

def evaluate_numeric(checks: list) -> bool:
    """
    Evaluate a list of numeric comparisons.

    Args:
        checks: list of tuples (name, actual_value, spec_value, operator_str)
                operator_str: '>=', '<=', '>', '<', '=='

    Returns:
        True if all checks pass, False otherwise

    Example:
        checks = [
            ('Thrust/Weight', 1.8, 1.5, '>='),
            ('Phase margin', 45.0, 30.0, '>='),
        ]
        result = evaluate_numeric(checks)
    """
    operators = {
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '==': lambda a, b: abs(a - b) < 1e-6,
    }

    all_pass = True
    print()
    print("Evaluation Results:")
    print("-" * 70)
    print(f"{'Metric':<30} {'Actual':<15} {'Spec':<15} {'Pass':<10}")
    print("-" * 70)

    for name, actual, spec, op_str in checks:
        op = operators[op_str]
        passed = op(actual, spec)
        status = "✓ PASS" if passed else "✗ FAIL"

        print(f"{name:<30} {actual:<15.3f} {spec_str(spec, op_str):<15} {status:<10}")

        if not passed:
            all_pass = False

    print("-" * 70)
    return all_pass

def spec_str(value, op_str):
    """Format spec value with operator."""
    return f"{op_str} {value:.3f}"
