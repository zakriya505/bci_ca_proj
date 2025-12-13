# Quick launcher for BCI Visualizer - Uses CSV Data
Write-Host "Launching BCI Waveform Visualizer..." -ForegroundColor Cyan
Write-Host "Loading data from: sample_eeg_data.csv" -ForegroundColor Green
Write-Host "(Close the window to exit)" -ForegroundColor Yellow
Write-Host ""

# Use the correct Python
$pythonCmd = "C:\Users\HAMZA SULTAN\AppData\Local\Programs\Python\Python312\python.exe"

if (-not (Test-Path $pythonCmd)) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    pause
    exit 1
}

# Set PYTHONPATH and run with CSV file
$env:PYTHONPATH = "$PWD\scripts"
& $pythonCmd scripts\visualizer_from_file.py sample_eeg_data.csv
