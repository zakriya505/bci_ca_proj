# Quick launcher for Attention Deficit Dataset Visualization
# This script visualizes EEG data specifically for attention deficit prediction

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "     BCI Attention Deficit Dataset Viewer" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Loading Attention Deficit Dataset..." -ForegroundColor Green
Write-Host "Focus: Theta/Beta ratio variations (attention)" -ForegroundColor Yellow
Write-Host ""

$DataFile = "data\raw\attention_deficit_data.csv"

# Check if dataset exists
if (-not (Test-Path $DataFile)) {
    Write-Host "ERROR: Dataset not found!" -ForegroundColor Red
    Write-Host "Generating datasets now..." -ForegroundColor Yellow
    Write-Host ""
    
    # Find Python
    $pythonCmd = $null
    $pythonPaths = @("python", "py")
    foreach ($path in $pythonPaths) {
        try {
            $result = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0 -or $result -match "Python") {
                $pythonCmd = $path
                break
            }
        } catch {}
    }
    
    if (-not $pythonCmd) {
        Write-Host "ERROR: Python not found!" -ForegroundColor Red
        pause
        exit 1
    }
    
    # Generate datasets
    & $pythonCmd scripts\generate_separate_datasets.py
    Write-Host ""
}

# Run visualizer
Write-Host "Starting visualization..." -ForegroundColor Green
Write-Host "(Close the window to exit)" -ForegroundColor Yellow
Write-Host ""

& .\run_from_file.ps1 $DataFile
