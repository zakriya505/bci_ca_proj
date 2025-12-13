# 🧠 BCI System - Quick Start

## Setup (First Time Only)
```powershell
.\setup_visualization.ps1
```

## Run the BCI Visualization
```powershell
# Test mode (simulated data - cycles through FOCUS, RELAX, BLINK)
.\run_visualizer.ps1

# OR load from CSV file
.\run_from_file.ps1 sample_eeg_data.csv
```

## What You'll See
- **EEG Waveform**: Green oscillating signal (top panel)
- **FFT Spectrum**: Alpha (8-13 Hz) and Beta (13-30 Hz) peaks
- **Feature Bars**: Yellow (Alpha) and Cyan (Beta) power
- **Status Panel**: 
  - Detected command: FOCUS, RELAX, or BLINK
  - LED: ON (green) or OFF (red)
  - Alpha and Beta power values

## How It Works
1. Brain generates electrical signals (EEG)
2. System analyzes frequencies:
   - **High Beta (13-30 Hz)** → FOCUS → LED ON
   - **High Alpha (8-13 Hz)** → RELAX → LED OFF
   - **Sharp spike** → BLINK → Buzzer
3. Visual display shows real-time analysis

## Files
- `run_visualizer.ps1` - Start the visualization
- `run_from_file.ps1` - Load custom CSV data
- `sample_eeg_data.csv` - Example EEG data (10 seconds, 2560 samples)
- `scripts/realtime_visualizer.py` - Main visualization code
- `scripts/visualizer_from_file.py` - CSV file loader

---

**For full project details, see README.md**
