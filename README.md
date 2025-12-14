# BCI - Brain-Computer Interface System

A Brain-Computer Interface implementation that detects mental commands from simulated EEG signals.

## What It Does

Detects 3 mental commands from brain signals:
- **FOCUS** (beta waves) → LED ON
- **RELAX** (alpha waves) → LED OFF  
- **BLINK** (spike) → Buzzer + Cursor moves

No hardware needed - uses simulated EEG data.

## Requirements

- **GCC** compiler
- **Python 3.x** with numpy, matplotlib, scipy (for visualization)
- **Conda** (recommended for Python environment)

## Build & Run

### Option 1: Native Windows Build (Recommended)

```bash
# Compile
gcc -I./include -o bin/bci_system.exe src/*.c -lm

# Run
./bin/bci_system.exe
```

### Option 2: Using Build Scripts

**PowerShell:**
```powershell
.\build_native.ps1
.\bin\bci_system.exe
```

**Git Bash:**
```bash
# Create bin directory if needed
mkdir -p bin

# Compile
gcc -I./include -o bin/bci_system.exe \
    src/main.c src/eeg_simulator.c src/preprocessing.c \
    src/feature_extraction.c src/classifier.c \
    src/output_control.c src/utils.c -lm

# Run
./bin/bci_system.exe
```

## Visualization

Run real-time BCI visualizer showing brain signals:

```bash
# Setup (first time only)
conda create -n bci python=3.11 -y
conda activate bci
pip install numpy matplotlib scipy pandas

# Run visualizer
python scripts/realtime_visualizer.py --test-mode
```

## Run Tests

Verify the system works correctly:

**Git Bash (Recommended):**
```bash
# Make test script executable
chmod +x tests/quick_test.sh

# Run all tests
./tests/quick_test.sh
```

**PowerShell:**
```powershell
.\tests\run_tests.ps1
```

**Manual Testing:**
```bash
# Compile tests
mkdir -p bin/tests
gcc -I./include -I./tests -o bin/tests/test_feature_extraction.exe \
    tests/test_feature_extraction.c src/feature_extraction.c src/utils.c -lm
gcc -I./include -I./tests -o bin/tests/test_classifier.exe \
    tests/test_classifier.c src/classifier.c src/utils.c -lm

# Run tests
./bin/tests/test_feature_extraction.exe
./bin/tests/test_classifier.exe
```

## Project Structure

```
bci_ca_proj/
├── src/           # C source files
├── include/       # Header files
├── tests/         # Unit tests
├── scripts/       # Python visualization
└── bin/           # Compiled executables
```

## Configuration

Edit `include/config.h` to adjust:
- Sampling rate (default: 256 Hz)
- Detection thresholds
- Debug options

## License

Academic project for educational purposes.
