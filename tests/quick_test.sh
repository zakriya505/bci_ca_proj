#!/bin/bash
# Quick compile and test script

cd /d/open_source/bci_ca_proj

echo "Compiling tests..."
mkdir -p bin/tests

# Compile
gcc -I./include -I./tests -o bin/tests/test_feature_extraction.exe \
    tests/test_feature_extraction.c src/feature_extraction.c src/utils.c -lm

gcc -I./include -I./tests -o bin/tests/test_classifier.exe \
    tests/test_classifier.c src/classifier.c src/utils.c -lm

echo "Running tests..."
echo ""

# Run
./bin/tests/test_feature_extraction.exe
result1=$?

./bin/tests/test_classifier.exe  
result2=$?

# Summary
echo ""
if [ $result1 -eq 0 ] && [ $result2 -eq 0 ]; then
    echo "✓ ALL TESTS PASSED!"
    exit 0
else
    echo "✗ SOME TESTS FAILED"
    exit 1
fi
