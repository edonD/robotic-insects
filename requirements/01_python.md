# Python & Core Scientific Packages

---

## Step 1: Install Python 3.9+

If you don't have Python, download from [python.org](https://www.python.org/downloads/) (version 3.9 or later).

Check your Python version:
```bash
python --version
```

---

## Step 2: Create a Virtual Environment

This keeps project dependencies isolated:

```bash
cd robotic-insects
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

---

## Step 3: Install Required Packages

Create a file called `requirements.txt` in the `robotic-insects/` directory:

```txt
numpy>=1.22
scipy>=1.8
matplotlib>=3.5
python-control>=0.9.0
allantools>=2021.11.1
sympy>=1.11
```

Then install:

```bash
pip install -r requirements.txt
```

---

## Step 4: Verify Installation

Run this Python script to check:

```python
import numpy as np
import scipy
import matplotlib
import control
import allantools
import sympy

print("✓ All Python packages installed successfully!")
print(f"  NumPy {np.__version__}")
print(f"  SciPy {scipy.__version__}")
print(f"  Matplotlib {matplotlib.__version__}")
print(f"  Control {control.__version__}")
```

Save as `check_python.py` and run:
```bash
python check_python.py
```

**Expected output:**
```
✓ All Python packages installed successfully!
  NumPy 1.22.x
  SciPy 1.8.x
  Matplotlib 3.5.x
  Control 0.9.x
```

---

## ✓ Python is Ready

Proceed to **02_ansys_cfd.md** for aerodynamics CFD solver.
