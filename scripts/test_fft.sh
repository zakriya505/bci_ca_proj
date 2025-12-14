#!/bin/bash
# Quick test script for FFT module

echo "========================================="
echo "Testing FFT Implementation"
echo "========================================="

# Create bin/tests directory if it doesn't exist
mkdir -p bin/tests

# Compile FFT test
echo "Compiling FFT test..."
gcc -I./include -I./tests -o bin/tests/test_fft.exe \
    tests/test_fft.c src/fft.c src/utils.c -lm

if [ $? -eq 0 ]; then
    echo "✓ Compilation successful"
    echo ""
    echo "Running FFT tests..."
    echo "========================================="
    ./bin/tests/test_fft.exe
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "========================================="
        echo "✓ All FFT tests passed!"
        echo "========================================="
    else
        echo ""
        echo "✗ Some tests failed"
        exit 1
    fi
else
    echo "✗ Compilation failed"
    exit 1
fi
