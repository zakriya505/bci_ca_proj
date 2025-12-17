# BCI Separate Datasets - User Guide

## Overview

The BCI project now uses **three separate datasets** for each prediction type:
- **visual_impairment_data.csv** - Focuses on visual impairment prediction (alpha power)
- **motor_impairment_data.csv** - Focuses on motor impairment prediction (beta power)  
- **attention_deficit_data.csv** - Focuses on attention deficit prediction (theta/beta ratio)

Each dataset is optimized to demonstrate its specific prediction type with realistic variations.

## Quick Start

### Generate All Datasets
```powershell
python scripts/generate_separate_datasets.py
```

This creates all three CSV files in `data/raw/` directory.

### Run Individual Visualizations

**Visual Impairment Dataset:**
```powershell
.\run_visual_impairment.ps1
```

**Motor Impairment Dataset:**
```powershell
.\run_motor_impairment.ps1
```

**Attention Deficit Dataset:**
```powershell
.\run_attention_deficit.ps1
```

### View All Datasets Together
```powershell
python scripts/visualize_all_predictions.py
```

Shows side-by-side comparison of all three datasets and their predictions.

## Dataset Details

### Visual Impairment Dataset
- **Focus:** Alpha power (8-13 Hz)
- **Location:** `data/raw/visual_impairment_data.csv`
- **Prediction:** Based on alpha band activity in occipital lobe
- **Timeline:**
  - 0-4s: NORMAL (high alpha)
  - 4-6s: BORDERLINE (medium alpha)
  - 6-10s: IMPAIRED (low alpha)

### Motor Impairment Dataset
- **Focus:** Beta power (13-30 Hz)
- **Location:** `data/raw/motor_impairment_data.csv`
- **Prediction:** Based on beta/mu rhythm in motor cortex
- **Timeline:**
  - 0-4s: NORMAL (high beta)
  - 4-6s: BORDERLINE (medium beta)
  - 6-10s: IMPAIRED (low beta)

### Attention Deficit Dataset
- **Focus:** Theta/Beta ratio (4-8 Hz / 13-30 Hz)
- **Location:** `data/raw/attention_deficit_data.csv`
- **Prediction:** Based on theta/beta ratio in frontal lobe
- **Timeline:**
  - 0-4s: NORMAL (low ratio ~0.5-1.0)
  - 4-6s: BORDERLINE (medium ratio ~1.75)
  - 6-10s: IMPAIRED (high ratio ~2.5-5.0)

## CSV Format

Each dataset contains the following columns:
- `time` - Timestamp in seconds
- `amplitude` - Composite EEG signal amplitude
- `theta_power` - Normalized theta band power (0-1)
- `alpha_power` - Normalized alpha band power (0-1)
- `beta_power` - Normalized beta band power (0-1)
- `gamma_power` - Normalized gamma band power (0-1)
- `command` - Detected mental command (NONE, FOCUS, RELAX, BLINK)
- `[prediction_type]` - Specific prediction (NORMAL, BORDERLINE, IMPAIRED)

## Visualization Features

When you run any of the launcher scripts, the visualization will:
- Display the dataset name in the window title
- Show "Dataset: [Type]" in the bottom system info
- Highlight the relevant prediction in the health panel
- Show all frequency bands and their variations over time

## Custom Datasets

You can also manually specify a dataset using:
```powershell
.\run_from_file.ps1 path\to\your_dataset.csv
```

The visualizer will automatically detect the prediction type from the filename if it contains "visual", "motor", or "attention".

## Troubleshooting

**Datasets not found:**
Run `python scripts/generate_separate_datasets.py` to generate them.

**Python not found:**
Run `.\setup_visualization.ps1` first to set up the Python environment.

**Visualization not showing:**
Ensure you have matplotlib and pandas installed:
```powershell
pip install matplotlib pandas numpy
```

## For Developers

### Adding New Datasets

1. Create new CSV file in `data/raw/` following the format above
2. Add prediction column (e.g., `new_prediction`)
3. Update health predictions section in C code if needed
4. Create new launcher script following the existing patterns

### Modifying Data Generation

Edit `scripts/generate_separate_datasets.py` to:
- Change frequency band amplitudes
- Adjust prediction thresholds
- Modify scenario timelines
- Add new frequency bands

---

**Questions?** Check the main README.md or inspect the existing datasets for examples.
