# Clean script for RISC-V BCI System (Windows PowerShell)

Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan

# Remove build directories
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
    Write-Host "  Removed build/" -ForegroundColor Green
}

if (Test-Path "bin") {
    Remove-Item -Recurse -Force bin
    Write-Host "  Removed bin/" -ForegroundColor Green
}

Write-Host "Clean complete!" -ForegroundColor Green
