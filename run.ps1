# Run script for RISC-V BCI System (Windows PowerShell)

Write-Host "Running RISC-V BCI System on QEMU..." -ForegroundColor Cyan
Write-Host ""

# Check if binary exists
if (-not (Test-Path "bin/bci_system.elf")) {
    Write-Host "Error: Binary not found!" -ForegroundColor Red
    Write-Host "Please run build.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Find QEMU executable
$qemuCmd = $null
$qemuPaths = @(
    "qemu-system-riscv32",
    "C:\Program Files\qemu\qemu-system-riscv32.exe",
    "C:\Program Files (x86)\qemu\qemu-system-riscv32.exe",
    "$env:ProgramFiles\qemu\qemu-system-riscv32.exe",
    "$env:LOCALAPPDATA\Programs\QEMU\qemu-system-riscv32.exe"
)

foreach ($path in $qemuPaths) {
    try {
        if ($path -like "*\*") {
            if (Test-Path $path) {
                $qemuCmd = $path
                break
            }
        } else {
            $result = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $qemuCmd = $path
                break
            }
        }
    } catch {}
}

if (-not $qemuCmd) {
    Write-Host "Error: QEMU RISC-V not found!" -ForegroundColor Red
    Write-Host "Please install QEMU and add to PATH" -ForegroundColor Yellow
    Write-Host "Install with: choco install qemu" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or download from: https://qemu.weilnetz.de/w64/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found QEMU at: $qemuCmd" -ForegroundColor Green
Write-Host "Press Ctrl+A then X to exit QEMU" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run on QEMU
& $qemuCmd -machine virt -nographic -bios none -kernel bin/bci_system.elf

