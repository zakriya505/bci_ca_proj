# 🎨 BCI Visual Display Guide

## See Your BCI in Action with LED Visualization!

I've created a Python GUI that shows:
- 🟢 **LED blinking** in real-time (green when ON, gray when OFF)
- 🧠 **Current command** (FOCUS, RELAX, BLINK)
- 🔔 **Buzzer activation** (animated beep)
- 📍 **Cursor position** (X, Y coordinates)
- 📜 **Activity log** (all events)

## 🚀 How to Run

### Step 1: Make Sure You Have Python

```powershell
python --version
```

If not installed, download from: https://www.python.org/downloads/

### Step 2: Run the Visualizer

```powershell
cd "e:\SEECS CS Data\Semester 5,Fall 2025\due_sem_proj\CA_proj\proj_dirs\proj_version_zero"
python scripts\bci_visualizer.py
```

### Step 3: Click "▶ Start BCI System"

The GUI will:
1. Open with a dark theme
2. Show a big LED circle (gray = OFF)
3. Display current command
4. Show activity log

Click the **"▶ Start BCI System"** button and watch:
- LED turns **GREEN** when FOCUS detected
- LED turns **GRAY** when RELAX detected
- **"♪ BEEP! ♪"** appears when BLINK detected
- Cursor position updates
- Activity log shows all events

## 🎯 What You'll See

```
╔══════════════════════════════════════╗
║  🧠 RISC-V Brain-Computer Interface  ║
╠══════════════════════════════════════╣
║                                      ║
║  LED Status:    ⚫ OFF               ║
║                 (or 🟢 ON)           ║
║                                      ║
║  Current Command:   FOCUS            ║
║                                      ║
║  ♪ BEEP! ♪  (when blink detected)   ║
║                                      ║
║  Cursor Position: (1, 0)             ║
║                                      ║
║  Activity Log:                       ║
║  ✓ LED turned ON                     ║
║  🔔 Buzzer activated!                ║
║  → Cursor moved to (1, 0)            ║
╚══════════════════════════════════════╝

[▶ Start BCI System]  [⏹ Stop]
```

## 📊 Features

### LED Display
- **Gray circle** = LED OFF (RELAX state)
- **Green circle** = LED ON (FOCUS state)
- Smooth color transitions

### Command Display
- **FOCUS** = Green text
- **RELAX** = Blue text
- **BLINK** = Orange text
- **NONE** = Yellow text

### Buzzer Animation
- Shows **"♪ BEEP! ♪"** for 500ms
- Appears when blink detected

### Activity Log
- Real-time event logging
- Auto-scrolls to latest
- Shows all state changes

## 🎮 Controls

| Button | Action |
|--------|--------|
| ▶ Start BCI System | Runs the BCI and shows visualization |
| ⏹ Stop | Stops the BCI system |

## 🔧 Troubleshooting

### "python not found"
Install Python: https://www.python.org/downloads/

### GUI doesn't open
Make sure you're in the project directory:
```powershell
cd "e:\SEECS CS Data\Semester 5,Fall 2025\due_sem_proj\CA_proj\proj_dirs\proj_version_zero"
```

### No output shown
Make sure `bin\bci_system.exe` exists:
```powershell
.\build_native.ps1
```

## 📸 Take Screenshots!

The GUI is perfect for:
- Project demonstrations
- Screenshots for reports
- Video recordings
- Live presentations

Just run it and capture the screen!

---

**Now you can SEE your BCI working in real-time!** 🎉
