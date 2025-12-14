#!/bin/bash
# Test Runner Script for BCI Project (Git Bash compatible)
# Compiles and runs all test suites

echo "BCI System - Test Runner"
echo "========================="
echo ""

# Create test output directory
testDir="tests"
binDir="bin/tests"

mkdir -p "$binDir"

# Find GCC
gcc_cmd="gcc"
if ! command -v "$gcc_cmd" &> /dev/null; then
    echo "ERROR: GCC not found!"
    exit 1
fi

echo "Compiling tests..."

# Test 1: Feature Extraction Tests
echo ""
echo "Building test_feature_extraction..."
$gcc_cmd -I./include -I./tests \
    -o "$binDir/test_feature_extraction.exe" \
    tests/test_feature_extraction.c \
    src/feature_extraction.c \
    src/utils.c \
    -lm

if [ $? -ne 0 ]; then
    echo "Failed to compile test_feature_extraction"
    exit 1
fi

# Test 2: Classifier Tests
echo "Building test_classifier..."
$gcc_cmd -I./include -I./tests \
    -o "$binDir/test_classifier.exe" \
    tests/test_classifier.c \
    src/classifier.c \
    src/utils.c \
    -lm

if [ $? -ne 0 ]; then
    echo "Failed to compile test_classifier"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Running Test Suites"
echo "═══════════════════════════════════════════════════════════════"

totalFailed=0

# Run Feature Extraction Tests
echo ""
echo "[1/2] Feature Extraction Tests"
"$binDir/test_feature_extraction.exe"
if [ $? -eq 0 ]; then
    echo "✓ Feature Extraction Tests PASSED"
else
    echo "✗ Feature Extraction Tests FAILED"
    totalFailed=$((totalFailed + 1))
fi

# Run Classifier Tests
echo ""
echo "[2/2] Classifier Tests"
"$binDir/test_classifier.exe"
if [ $? -eq 0 ]; then
    echo "✓ Classifier Tests PASSED"
else
    echo "✗ Classifier Tests FAILED"
    totalFailed=$((totalFailed + 1))
fi

# Final Summary
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Test Summary"
echo "═══════════════════════════════════════════════════════════════"

if [ $totalFailed -eq 0 ]; then
    echo ""
    echo "ALL TESTS PASSED! ✓"
else
    echo ""
    echo "SOME TESTS FAILED! ($totalFailed test suites)"
fi

echo ""

exit $totalFailed
