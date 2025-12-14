#!/bin/bash
# Simpler build script for the integration demo

echo "Building Integration Demo..."
mkdir -p bin

gcc -I./include -o bin/demo_integration.exe \
    src/demo_integration.c \
    src/data_loader.c \
    src/fft.c \
    src/lda.c \
    src/feature_extraction.c \
    src/utils.c \
    -lm

if [ $? -eq 0 ]; then
    echo "Build successful! Run with: ./bin/demo_integration.exe"
else
    echo "Build failed."
    exit 1
fi
