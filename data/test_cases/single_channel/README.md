# Single-Channel Test Cases

This directory contains focused single-channel test datasets for unit testing specific BCI features.

## Test Data Files

### Focus Test Data
- **File**: `focus_baseline.csv`
- **Description**: Pure FOCUS command signal (high beta, low alpha)
- **Duration**: ~2 seconds
- **Use**: Test beta band detection and FOCUS classification

### Relax Test Data
- **File**: `relax_baseline.csv`
- **Description**: Pure RELAX command signal (high alpha, low beta)
- **Duration**: ~2 seconds
- **Use**: Test alpha band detection and RELAX classification

### Blink Test Data
- **File**: `blink_events.csv`
- **Description**: Multiple BLINK artifact events
- **Duration**: ~2 seconds
- **Use**: Test peak detection and BLINK classification

### Noise Test Data
- **File**: `high_noise.csv`
- **Description**: Signal with increased noise level
- **Duration**: ~2 seconds
- **Use**: Test robustness of preprocessing and feature extraction

## Generating Test Data

Use the script to generate these test files:

```bash
# Generate all single-channel test cases
python scripts/generate_test_data.py --output data/test_cases/single_channel/
```

## Format

All test cases use the standard CSV format:
```csv
time,amplitude,alpha_power,beta_power,command
0.000,10.5,0.3,0.7,FOCUS
...
```
