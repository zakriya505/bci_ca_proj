# Quick launcher for BCI Visualizer with File Input
# Usage: .\run_from_file.ps1 sample_eeg_data_full.csv

param(
    [string]$FilePath = "sample_eeg_data.csv"
)

Write-Host "Loading EEG data from file: $FilePath" -ForegroundColor Cyan

# Find Python (same logic as other scripts)
$pythonPaths = @(
    "python",
    "py",
    "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
    "C:\Python*\python.exe"
)

$pythonCmd = $null
foreach ($path in $pythonPaths) {
    try {
        if ($path -like "*\*") {
            $found = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $pythonCmd = $found.FullName
                break
            }
        } else {
            $result = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0 -or $result -match "Python") {
                $pythonCmd = $path
                break
            }
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please run: .\setup_visualization.ps1 first" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "(Close the window to exit)" -ForegroundColor Yellow
Write-Host ""

# Set PYTHONPATH to include scripts directory
$env:PYTHONPATH = "$PWD\scripts"

& $pythonCmd scripts\visualizer_from_file.py $FilePath
