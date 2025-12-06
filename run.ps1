# Run script for RISC-V BCI System (Windows PowerShell)

Write-Host "Running RISC-V BCI System on QEMU..." -ForegroundColor Cyan
Write-Host ""

# Check if binary exists
if (-not (Test-Path "bin/bci_system.elf")) {
    Write-Host "Error: Binary not found!" -ForegroundColor Red
    Write-Host "Please run build.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check if QEMU is available
try {
    & qemu-system-riscv32 --version | Out-Null
} catch {
    Write-Host "Error: QEMU RISC-V not found!" -ForegroundColor Red
    Write-Host "Please install QEMU and add to PATH" -ForegroundColor Yellow
    Write-Host "Install with: choco install qemu" -ForegroundColor Yellow
    exit 1
}

Write-Host "Press Ctrl+A then X to exit QEMU" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run on QEMU
& qemu-system-riscv32 -machine virt -nographic -bios none -kernel bin/bci_system.elf
