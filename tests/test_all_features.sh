#!/bin/bash
# Master Test Script for BCI Project
# Runs all unit tests to verify system integrity

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}      BCI Project - System Verification  ${NC}"
echo -e "${BLUE}=========================================${NC}"

# Create bin directory if it doesn't exist
mkdir -p bin/tests

# Function to run a test
run_test() {
    test_name=$1
    source_files=$2
    
    echo -e "\n${BLUE}[TEST] $test_name${NC}"
    echo "-----------------------------------------"
    
    # Compile
    gcc -I./include -I./tests -o "bin/tests/${test_name}.exe" $source_files -lm
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Compilation successful${NC}"
        
        # Run
        "./bin/tests/${test_name}.exe"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Test PASSED${NC}"
            return 0
        else
            echo -e "${RED}✗ Test FAILED${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Compilation FAILED${NC}"
        return 1
    fi
}

# 1. Test Data Loader
run_test "test_data_loader" "tests/test_data_loader.c src/data_loader.c src/utils.c"
status_loader=$?

# 2. Test FFT and PSD
run_test "test_fft" "tests/test_fft.c src/fft.c src/utils.c"
status_fft=$?

# 3. Test LDA Classifier
run_test "test_lda" "tests/test_lda_classifier.c src/lda.c src/utils.c"
status_lda=$?

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${BLUE}           Summary Results               ${NC}"
echo -e "${BLUE}=========================================${NC}"

if [ $status_loader -eq 0 ]; then echo -e "Data Loader:  ${GREEN}PASS${NC}"; else echo -e "Data Loader:  ${RED}FAIL${NC}"; fi
if [ $status_fft -eq 0 ];    then echo -e "FFT Engine:   ${GREEN}PASS${NC}"; else echo -e "FFT Engine:   ${RED}FAIL${NC}"; fi
if [ $status_lda -eq 0 ];    then echo -e "LDA Model:    ${GREEN}PASS${NC}"; else echo -e "LDA Model:    ${RED}FAIL${NC}"; fi

echo -e "========================================="
