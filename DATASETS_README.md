# Quick Reference - Separate Datasets Feature

## What's New?
Three specialized EEG datasets for different prediction types:
- `visual_impairment_data.csv` - Alpha power variations
- `motor_impairment_data.csv` - Beta power variations
- `attention_deficit_data.csv` - Theta/Beta ratio variations

## Quick Start

### Generate Datasets (First Time)
```bash
python scripts/generate_separate_datasets.py
```

### Run Visualizations
```powershell
# Visual impairment
.\run_visual_impairment.ps1

# Motor impairment
.\run_motor_impairment.ps1

# Attention deficit
.\run_attention_deficit.ps1

# View all together
python scripts/visualize_all_predictions.py
```

## Files Created
- `scripts/generate_separate_datasets.py` - Dataset generator
- `scripts/visualize_all_predictions.py` - Combined visualization
- `run_visual_impairment.ps1` - Visual dataset launcher
- `run_motor_impairment.ps1` - Motor dataset launcher
- `run_attention_deficit.ps1` - Attention dataset launcher
- `DATASETS_GUIDE.md` - Complete user guide

## See Also
- [DATASETS_GUIDE.md](DATASETS_GUIDE.md) - Detailed documentation
- [Walkthrough](walkthrough.md) - Implementation details
