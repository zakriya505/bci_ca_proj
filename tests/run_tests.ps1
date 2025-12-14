# Test Runner Script for BCI Project
# Compiles and runs all test suites

Write-Host "BCI System - Test Runner" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Create test output directory
$testDir = "tests"
$binDir = "bin\tests"

if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Force -Path $binDir | Out-Null
}

# Find GCC
$gcc = "gcc"
try {
    & $gcc --version | Out-Null
} catch {
    Write-Host "ERROR: GCC not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Compiling tests..." -ForegroundColor Yellow

# Test 1: Feature Extraction Tests
Write-Host "`nBuilding test_feature_extraction..." -ForegroundColor Green
& $gcc -I./include -I./tests `
    -o "$binDir/test_feature_extraction.exe" `
    tests/test_feature_extraction.c `
    src/feature_extraction.c `
    src/utils.c `
    -lm

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to compile test_feature_extraction" -ForegroundColor Red
    exit 1
}

# Test 2: Classifier Tests
Write-Host "Building test_classifier..." -ForegroundColor Green
& $gcc -I./include -I./tests `
    -o "$binDir/test_classifier.exe" `
    tests/test_classifier.c `
    src/classifier.c `
    src/utils.c `
    -lm

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to compile test_classifier" -ForegroundColor Red
    exit 1
}

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Running Test Suites" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

$totalPassed = 0
$totalFailed = 0

# Run Feature Extraction Tests
Write-Host "`n[1/2] Feature Extraction Tests" -ForegroundColor Magenta
& "$binDir/test_feature_extraction.exe"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Feature Extraction Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Feature Extraction Tests FAILED" -ForegroundColor Red
    $totalFailed++
}

# Run Classifier Tests
Write-Host "`n[2/2] Classifier Tests" -ForegroundColor Magenta
& "$binDir/test_classifier.exe"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Classifier Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Classifier Tests FAILED" -ForegroundColor Red
    $totalFailed++
}

# Final Summary
Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($totalFailed -eq 0) {
    Write-Host "`nALL TESTS PASSED! ✓" -ForegroundColor Green
} else {
    Write-Host "`nSOME TESTS FAILED! ($totalFailed test suites)" -ForegroundColor Red
}

Write-Host ""

exit $totalFailed
