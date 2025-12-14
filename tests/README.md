# BCI System - Test Suite

## Overview

Comprehensive unit tests for the Brain-Computer Interface system to verify correctness of signal processing and classification.

## Test Coverage

### 1. Feature Extraction Tests (`test_feature_extraction.c`)
- ✅ Alpha band power calculation
- ✅ Beta band power calculation  
- ✅ Feature normalization
- ✅ Peak amplitude detection
- ✅ Variance calculation
- ✅ Edge cases (zero signal)

### 2. Classifier Tests (`test_classifier.c`)
- ✅ FOCUS command detection
- ✅ RELAX command detection
- ✅ BLINK command detection
- ✅ Command priority (BLINK > FOCUS > RELAX)
- ✅ Debouncing logic
- ✅ Baseline amplitude updates

## Running Tests

### Git Bash (Recommended for MINGW64)
```bash
cd d:/open_source/bci_ca_proj
./tests/run_tests.sh
```

### PowerShell (Windows)
```powershell
cd d:\open_source\bci_ca_proj
.\tests\run_tests.ps1
```

### Manual Compilation
```bash
# Feature extraction tests
gcc -I./include -I./tests -o bin/tests/test_feature_extraction.exe \
    tests/test_feature_extraction.c src/feature_extraction.c src/utils.c -lm

# Classifier tests  
gcc -I./include -I./tests -o bin/tests/test_classifier.exe \
    tests/test_classifier.c src/classifier.c src/utils.c -lm

# Run tests
./bin/tests/test_feature_extraction.exe
./bin/tests/test_classifier.exe
```

## Test Results Format

```
╔════════════════════════════════════════════════════════════════╗
║ Test Suite: Feature Extraction Tests                          ║
╚════════════════════════════════════════════════════════════════╝

[TEST] Alpha Band Power Calculation
  ✓ PASS: Alpha power > Beta power for 10Hz signal
  ✓ PASS: Alpha power is positive

════════════════════════════════════════════════════════════════
Test Results:
  Total:  18
  Passed: 18 (100.0%)
  Failed: 0
════════════════════════════════════════════════════════════════
```

## Adding New Tests

1. Create test file in `tests/` directory
2. Include `test_framework.h`
3. Write test functions
4. Add to `run_tests.ps1`

Example:
```c
#include "test_framework.h"
#include "../include/your_module.h"

void test_something() {
    TEST_START("Something Test");
    ASSERT_TRUE(1 == 1, "Math works");
}

int main() {
    TEST_SUITE_START("Your Tests");
    test_something();
    TEST_SUITE_END();
    return tests_failed > 0 ? 1 : 0;
}
```

## Assertions Available

- `ASSERT_TRUE(condition, message)` - Check boolean condition
- `ASSERT_EQUAL(expected, actual, message)` - Check integer equality
- `ASSERT_FLOAT_EQUAL(expected, actual, tolerance, message)` - Check float equality with tolerance

## Continuous Testing

Run tests after any code changes to ensure correctness:
```powershell
# Quick test
.\tests\run_tests.ps1

# If tests pass, rebuild main system
.\build_native.ps1
```
