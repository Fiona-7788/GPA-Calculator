# 🎓 GPA Calculator

A Python tool for tracking courses and computing weighted GPA, built as a COGS 18 final project at UC San Diego.

## 📋 Features
- Track courses and letter grades across a quarter or semester
- Compute weighted cumulative GPA automatically
- Simulate how a future course affects your GPA (what-if analysis)
- Visualize grades as a bar chart with a GPA reference line
- Save and load student data to a JSON file for persistent storage

## 📁 Project Structure
GPA-Calculator/
├── ProjectNotebook.ipynb  ← demo, testing, and project description
├── gpa_module.py          ← Student class and helper functions
├── test_gpa.py            ← 27 unit tests using unittest
├── script.py              ← runnable demo script
└── requirements.txt       ← dependencies

## ⚙️ Installation
```bash
pip install matplotlib
```

## 🚀 How to Run

**Option 1 — Script:**
```bash
python script.py
```

**Option 2 — Jupyter Notebook:**
```bash
jupyter notebook ProjectNotebook.ipynb
```

## 🧪 How to Run Tests
```bash
python -m unittest test_gpa.py -v
```
27 tests — all passing ✅

## 💡 Example Usage
```python
from gpa_module import Student

student = Student("Alex")
student.add_course("COGS 18", "A", 4)
student.add_course("MATH 20A", "B+", 4)
student.add_course("WCWP 10A", "A-", 4)

student.display_transcript()
# Student: Alex
# ----------------------------------------
# Course               Grade    Units
# ----------------------------------------
# COGS 18              A        4
# MATH 20A             B+       4
# WCWP 10A             A-       4
# ----------------------------------------
# Cumulative GPA: 3.65

print(student.what_if("A", 4))  # → 3.74 (simulated)
student.plot_grades()            # bar chart
student.save("alex.json")        # save to file
```

## 🛠️ Technologies
- Python 3
- `matplotlib` — grade visualization
- `json` — persistent data storage (built-in)
- `unittest` — testing framework (built-in)
