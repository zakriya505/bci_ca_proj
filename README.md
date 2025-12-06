# RISC-V Brain-Computer Interface (BCI) System

A complete Brain-Computer Interface implementation for RISC-V architecture that detects mental commands from simulated EEG signals.

## 🎯 What This Does

This BCI system:
- **Simulates brain signals** (EEG waves - no hardware needed!)
- **Detects 3 mental commands**:
  - **FOCUS** (beta waves 13-30 Hz) → LED turns ON ✅
  - **RELAX** (alpha waves 8-13 Hz) → LED turns OFF ⭕
  - **BLINK** (sharp spike) → Buzzer + Cursor moves 🔔
- **Runs on RISC-V** using QEMU simulator
- **Helps paralyzed people** control devices with brain activity alone

## 🚀 Quick Start

### 1. Install RISC-V Toolchain

**Download (104 MB):**
```
https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/download/v15.2.0-1/xpack-riscv-none-elf-gcc-15.2.0-1-win32-x64.zip
```

**Extract:**
```powershell
New-Item -ItemType Directory -Force -Path "C:\riscv"
Expand-Archive -Path "$env:USERPROFILE\Downloads\xpack-riscv-none-elf-gcc-15.2.0-1-win32-x64.zip" -DestinationPath "C:\riscv"
```

**Add to PATH (Run PowerShell as Administrator):**
```powershell
$currentPath = [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$newPath = $currentPath + ";C:\riscv\xpack-riscv-none-elf-gcc-15.2.0-1\bin"
[Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
```

**Verify (restart PowerShell first):**
```powershell
riscv-none-elf-gcc --version
```

### 2. Install QEMU (Simulator)

```powershell
choco install qemu
```

Or download from: https://qemu.weilnetz.de/w64/

### 3. Build & Run

**Option A: Native Windows Build (Easiest - See Output Immediately)**

```powershell
cd "e:\SEECS CS Data\Semester 5,Fall 2025\due_sem_proj\CA_proj\proj_dirs\proj_version_zero"
.\build_native.ps1
.\bin\bci_system.exe
```

This builds and runs directly on Windows - you'll see all the output!

**Option B: RISC-V Build (For RISC-V Demonstration)**

```powershell
.\build.ps1
.\run.ps1
```

**Exit QEMU:** Press `Ctrl+A`, then `X`

## 📁 Project Structure

```
proj_version_zero/
├── src/                    # Source code
│   ├── main.c              # Main program
│   ├── eeg_simulator.c     # Signal generation
│   ├── preprocessing.c     # Signal filtering (C)
│   ├── preprocessing_asm.S # Optimized filters (RISC-V Assembly)
│   ├── feature_extraction.c
│   ├── feature_extraction_asm.S
│   ├── classifier.c
│   ├── output_control.c
│   └── utils.c
├── include/                # Header files
├── scripts/                # Python visualization
├── build.ps1              # Build script
├── run.ps1                # Run script
├── clean.ps1              # Clean script
└── Makefile               # Build system
```

## 🎮 What You'll See

The system runs 4 demo scenarios:

### 1. FOCUS Demo (5 iterations)
```
[FEATURES]
  Alpha Power:     0.2314
  Beta Power:      0.7686  ← High beta!
  
Detected: FOCUS ✓

╔════════════════════════════════════════════╗
║          OUTPUT DEVICE STATUS              ║
╠════════════════════════════════════════════╣
║ [LED] ████████ ON                          ║
╚════════════════════════════════════════════╝
```

### 2. RELAX Demo (5 iterations)
```
[FEATURES]
  Alpha Power:     0.7686  ← High alpha!
  Beta Power:      0.2314
  
Detected: RELAX ✓

║ [LED] ░░░░░░░░ OFF                         ║
```

### 3. BLINK Demo (5 iterations)
```
[FEATURES]
  Peak Amplitude:  198.45  ← Sharp spike!
  
Detected: BLINK ✓

║ [BUZZER] ♪ BEEP! ♪                         ║
║ Cursor Position: (1, 0)                    ║
```

### 4. Interactive Mixed Demo
All commands in sequence showing real-world usage.

## 🔧 System Architecture

```
EEG Signal → Preprocessing → Feature Extraction → Classification → Output Control
   (C)          (C + ASM)        (C + ASM)            (C)              (C)
```

**Signal Processing Pipeline:**
1. Generate synthetic EEG (alpha/beta waves, blink artifacts)
2. Filter noise with moving average
3. Extract features (band power, peak amplitude, variance)
4. Classify command using thresholds
5. Control virtual devices (LED, buzzer, cursor)

**RISC-V Assembly Optimizations:**
- Moving average filter (`preprocessing_asm.S`)
- Power & variance calculation (`feature_extraction_asm.S`)
- Uses `rv32imf` ISA (32-bit integer, multiply, float)

## 📊 Configuration

Edit `include/config.h` to adjust:

```c
#define SAMPLING_RATE       256     // Hz
#define FOCUS_THRESHOLD     0.6     // Beta power ratio
#define RELAX_THRESHOLD     0.6     // Alpha power ratio
#define BLINK_THRESHOLD     3.0     // Amplitude multiplier
```

## 🎓 Why This Matters

### Helps Paralyzed People
- People with ALS/paralysis can't move or speak
- This lets them control devices with **brain activity only**
- Can select letters, trigger actions, communicate

### Educational Value
- Learn **RISC-V assembly** programming
- Understand **signal processing** (filtering, feature extraction)
- Practice **embedded systems** design
- Study **assistive technology** applications

### Open & Affordable
- Commercial BCIs cost **$10,000+**
- This is **free, open-source, simulation-based**
- Anyone can learn and customize

## 📈 Technical Details

**Language Distribution:**
- C: ~70% (signal processing, classification)
- RISC-V Assembly: ~25% (optimized filters)
- Python: ~5% (visualization)

**Performance:**
- Real-time capable at 256 Hz sampling
- ~2KB memory for signal buffers
- ~50KB binary size (optimized)

**Signal Parameters:**
- Sampling Rate: 256 Hz
- Window Size: 256 samples (1 second)
- Alpha Band: 8-13 Hz (relaxation)
- Beta Band: 13-30 Hz (focus)

## 🧪 Optional: Visualize Signals

```powershell
cd scripts
pip install numpy matplotlib
python visualize.py
```

Creates plots showing brain signals and frequency spectrum.

## 🆘 Troubleshooting

**"riscv-none-elf-gcc not found"**
- Verify PATH: `$env:Path -split ';' | Select-String riscv`
- Restart PowerShell
- Check file exists: `Test-Path "C:\riscv\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe"`

**Build errors**
- Ensure toolchain supports `rv32imf` ISA
- Run `.\clean.ps1` then `.\build.ps1`

**QEMU not starting**
- Install QEMU: `choco install qemu`
- Verify: `qemu-system-riscv32 --version`

## 📚 Academic Context

**Course:** CS339 - Computer Architecture  
**Institution:** SEECS  
**Semester:** Fall 2025

**Learning Objectives:**
- RISC-V ISA programming
- Embedded system design
- Signal processing algorithms
- Hardware-software co-design
- Assistive technology applications

## 📝 Quick Commands

| Action | Command |
|--------|---------|
| Build | `.\build.ps1` |
| Run | `.\run.ps1` |
| Clean | `.\clean.ps1` |
| Rebuild | `.\clean.ps1; .\build.ps1` |

## 📧 License

This is an academic project for educational purposes.

---

**Ready to see your BCI in action?** Run `.\build.ps1` then `.\run.ps1`! 🎉
