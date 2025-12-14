# Multi-Channel Test Cases

This directory will contain multi-channel (8-16 channels) test datasets for testing advanced BCI features.

## Future Test Data Files

### Motor Imagery Test Data
- **File**: `motor_imagery_8ch.csv` (to be created)
- **Channels**: 8
- **Description**: Left/right hand motor imagery
- **Use**: Test CSP and multi-channel classification

### Synchronized Multi-Channel
- **File**: `sync_multichannel_16ch.csv` (to be created)
- **Channels**: 16
- **Description**: Synchronized signals across all channels
- **Use**: Test parallel processing and threading

## Format

Multi-channel CSV format:
```csv
time,ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,command
0.000,10.5,12.3,8.7,15.2,9.8,11.4,13.6,10.9,FOCUS
...
```

## Note

Multi-channel test data will be generated when multi-channel support is implemented.
