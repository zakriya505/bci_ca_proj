# Build script for native Windows execution (for visualization)

Write-Host "Building BCI System for Windows (Native)..." -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Force -Path build, bin | Out-Null

# Use native GCC (MinGW or MSVC)
$CC = "gcc"
$CFLAGS = "-O2", "-Wall", "-Iinclude", "-lm"

# Check if GCC is available
try {
    & $CC --version | Out-Null
}
catch {
    Write-Host "Error: GCC not found!" -ForegroundColor Red
    Write-Host "Installing MinGW GCC..." -ForegroundColor Yellow
    Write-Host "Run: choco install mingw" -ForegroundColor Yellow
    exit 1
}

Write-Host "Compiling C source files..." -ForegroundColor Green

# Get all C files except assembly-dependent ones and demo_integration (has its own main)
$cFiles = @(
    "src/main.c",
    "src/eeg_simulator.c",
    "src/preprocessing.c",
    "src/feature_extraction.c",
    "src/classifier.c",
    "src/output_control.c",
    "src/utils.c",
    "src/fft.c",
    "src/lda.c",
    "src/data_loader.c"
)

$objFiles = @()

foreach ($file in $cFiles) {
    if (Test-Path $file) {
        $basename = [System.IO.Path]::GetFileNameWithoutExtension($file)
        $objFile = "build/$basename.o"
        Write-Host "  $file -> $objFile"
        & $CC -c $file -o $objFile -Iinclude -O2 -Wall
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error compiling $file" -ForegroundColor Red
            exit 1
        }
        $objFiles += $objFile
    }
}

Write-Host "Linking..." -ForegroundColor Green

# Link all object files
& $CC -o bin/bci_system.exe $objFiles -lm

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error linking" -ForegroundColor Red
    exit 1
}

Write-Host "Build successful!" -ForegroundColor Green
Write-Host "Output: bin/bci_system.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run: .\bin\bci_system.exe" -ForegroundColor Yellow
