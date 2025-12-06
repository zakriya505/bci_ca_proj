# Build script for RISC-V BCI System (Windows PowerShell)

Write-Host "Building RISC-V BCI System..." -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Force -Path build, bin | Out-Null

# Compiler settings (xPack toolchain)
$CC = "riscv-none-elf-gcc"
$AS = "riscv-none-elf-as"
$CFLAGS = "-march=rv32imf", "-mabi=ilp32f", "-O2", "-Wall", "-Wextra", "-Iinclude"
$ASFLAGS = "-march=rv32imf", "-mabi=ilp32f"

# Check if toolchain is available
try {
    & $CC --version | Out-Null
}
catch {
    Write-Host "Error: RISC-V toolchain not found!" -ForegroundColor Red
    Write-Host "Please install riscv-none-elf-gcc (xPack) and add to PATH" -ForegroundColor Yellow
    Write-Host "See INSTALL_TOOLCHAIN.md for installation instructions" -ForegroundColor Yellow
    exit 1
}

Write-Host "Compiling C source files..." -ForegroundColor Green

# Compile C files
$cFiles = Get-ChildItem -Path src -Filter *.c
foreach ($file in $cFiles) {
    $objFile = "build/$($file.BaseName).o"
    Write-Host "  $($file.Name) -> $objFile"
    & $CC $CFLAGS -c $file.FullName -o $objFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error compiling $($file.Name)" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Assembling RISC-V assembly files..." -ForegroundColor Green

# Assemble .S files
$asmFiles = Get-ChildItem -Path src -Filter *.S
foreach ($file in $asmFiles) {
    $objFile = "build/$($file.BaseName).o"
    Write-Host "  $($file.Name) -> $objFile"
    & $AS $ASFLAGS $file.FullName -o $objFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error assembling $($file.Name)" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Linking..." -ForegroundColor Green

# Link all object files
$objFiles = Get-ChildItem -Path build -Filter *.o
& $CC -march=rv32imf -mabi=ilp32f -o bin/bci_system.elf $objFiles.FullName -lm

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error linking" -ForegroundColor Red
    exit 1
}

Write-Host "Build successful!" -ForegroundColor Green
Write-Host "Output: bin/bci_system.elf" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run: qemu-system-riscv32 -machine virt -nographic -bios none -kernel bin/bci_system.elf" -ForegroundColor Yellow
