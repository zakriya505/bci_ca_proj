# Quick Test Commands for Git Bash

## Compile Tests Manually

```bash
# From project root
cd /d/open_source/bci_ca_proj

# Create output directory
mkdir -p bin/tests

# Compile feature extraction tests
gcc -I./include -I./tests -o bin/tests/test_feature_extraction.exe \
    tests/test_feature_extraction.c src/feature_extraction.c src/utils.c -lm

# Compile classifier tests
gcc -I./include -I./tests -o bin/tests/test_classifier.exe \
    tests/test_classifier.c src/classifier.c src/utils.c -lm
```

## Run Tests

```bash
# Run feature extraction tests
./bin/tests/test_feature_extraction.exe

# Run classifier tests  
./bin/tests/test_classifier.exe
```

## Or Use PowerShell

If GCC issues persist in Git Bash, switch to PowerShell:

```powershell
cd d:\open_source\bci_ca_proj
.\tests\run_tests.ps1
```
