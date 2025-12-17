# Quick launcher for Motor Impairment Dataset Visualization
# This script visualizes EEG data specifically for motor impairment prediction

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "       BCI Motor Impairment Dataset Viewer" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Loading Motor Impairment Dataset..." -ForegroundColor Green
Write-Host "Focus: Beta power variations (motor control)" -ForegroundColor Yellow
Write-Host ""

$DataFile = "data\raw\motor_impairment_data.csv"

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

# Run specialized visualizer
Write-Host "Starting visualization..." -ForegroundColor Green
Write-Host "(Close the window to exit)" -ForegroundColor Yellow
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

& $pythonCmd scripts\visualizer_motor_impairment.py $DataFile

