# BCI - Brain-Computer Interface System

A Brain-Computer Interface implementation that detects mental commands from simulated EEG signals.

## What It Does

Detects mental commands from brain signals:
- **FOCUS** (beta waves) → LED ON
- **RELAX** (alpha waves) → LED OFF  
- **BLINK** (spike) → Buzzer + Cursor moves

Health predictions:
- **Visual Impairment** (alpha power)
- **Motor Impairment** (beta power)
- **Attention Deficit** (theta/beta ratio)

---

## Quick Start

### Step 1: Install Prerequisites

**Required:**
- GCC compiler (MinGW on Windows)
- Python 3.8+

**Check installation:**
```powershell
gcc --version
python --version
```

**Install if missing:**
```powershell
# Install MinGW GCC
choco install mingw

# Install Python (or download from python.org)
choco install python
```

---

### Step 2: Setup Python Environment

```powershell
cd "path\to\bci_ca_proj"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r scripts\requirements.txt
```

---

### Step 3: Generate EEG Datasets

```powershell
# Generate all sample datasets
python scripts\generate_separate_datasets.py
```

This creates:
- `data/raw/visual_impairment_data.csv`
- `data/raw/motor_impairment_data.csv`
- `data/raw/attention_deficit_data.csv`

---

### Step 4: Build the C Project

```powershell
# Build BCI system
.\build_native.ps1

# Verify executable created
Test-Path .\bin\bci_system.exe
```

---

### Step 5: Run Tests

```powershell
# Run all unit tests
.\tests\run_tests.ps1
```

Expected output: `ALL TESTS PASSED!`

---

### Step 6: Run Visualization

```powershell
# Launch unified visualizer (all modes)
.\run_visualizer.ps1
```

**Navigation buttons:**
- 📊 General EEG - Standard EEG visualization
- 👁️ Visual Impairment - Alpha band focus
- 🏃 Motor Impairment - Beta band focus
- 🎯 Attention Deficit - Theta/Beta ratio
- 📈 Compare All - Side-by-side comparison
- 🖥️ Complete CA View - **Full RISC-V Architecture Dashboard** with:
  - Instruction breakdown pie chart
  - C vs Assembly benchmark comparison
  - Pipeline visualization
  - Cache hit rate & branch prediction
  - Performance metrics (IPC, cycles, stalls)

---

## Complete Build Commands (Copy-Paste Ready)

```powershell
# Full setup from scratch
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r scripts\requirements.txt
python scripts\generate_separate_datasets.py
.\build_native.ps1
.\tests\run_tests.ps1
.\run_visualizer.ps1
```

---

## Project Structure

```
bci_ca_proj/
├── src/           # C source files (13 files)
├── include/       # Header files (11 files)
├── tests/         # Unit tests + run_tests.ps1
├── scripts/       # Python visualization scripts
├── data/raw/      # EEG datasets
└── bin/           # Compiled executables
```

---

## Configuration

Edit `include/config.h` to adjust:
- Sampling rate (default: 256 Hz)
- Detection thresholds
- Debug options

---

## Troubleshooting

**Python not found:**
- Install Python 3.8+ and add to PATH
- Use `python3` instead of `python` if needed

**GCC not found:**
- Install MinGW: `choco install mingw`
- Add to PATH: `C:\mingw64\bin`

**Visualization not showing:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r scripts\requirements.txt`

**Tests failing:**
- Clean build: `.\clean.ps1` then `.\build_native.ps1`

---

## License

Academic project for educational purposes.
