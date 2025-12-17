# BCI Unified Visualizer Launcher
# Launches the unified visualization interface with all modes

Write-Host "Launching BCI Unified Visualizer..." -ForegroundColor Cyan
Write-Host ""

# Find Python
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
    Write-Host "Please install Python 3.x and add to PATH" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Using Python: $pythonCmd" -ForegroundColor Green
Write-Host ""

# Set PYTHONPATH
$env:PYTHONPATH = "$PWD\scripts"

# Launch unified visualizer
& $pythonCmd scripts\unified_visualizer.py
