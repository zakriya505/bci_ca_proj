# Setup script for BCI Visualization
# Run this in PowerShell: .\setup_visualization.ps1

Write-Host "Setting up BCI Visualization System..." -ForegroundColor Cyan

# Find Python
$pythonPaths = @(
    "python",
    "python3",
    "py",
    "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
    "C:\Python*\python.exe"
)

$pythonCmd = $null
foreach ($path in $pythonPaths) {
    try {
        if ($path -like "*\*") {
            # It's a path pattern
            $found = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $pythonCmd = $found.FullName
                break
            }
        } else {
            # It's a command
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
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Found Python: $pythonCmd" -ForegroundColor Green

# Check version
$version = & $pythonCmd --version
Write-Host "Version: $version" -ForegroundColor Green

# Install packages
Write-Host "`nInstalling required packages..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

& $pythonCmd -m pip install numpy matplotlib scipy --upgrade

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install packages" -ForegroundColor Red
    Write-Host "Try running: $pythonCmd -m pip install --user numpy matplotlib scipy" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nTo run the visualizer:" -ForegroundColor Cyan
Write-Host "  $pythonCmd scripts\realtime_visualizer.py --test-mode" -ForegroundColor Yellow
Write-Host ""

# Test the visualizer
Write-Host "Would you like to test the visualizer now? (Y/N)" -ForegroundColor Cyan
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "`nLaunching visualizer..." -ForegroundColor Green
    & $pythonCmd scripts\realtime_visualizer.py --test-mode
}
