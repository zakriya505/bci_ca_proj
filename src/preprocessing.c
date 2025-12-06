#include "preprocessing.h"
#include "utils.h"
#include <math.h>
#include <string.h>

void preprocessing_init(void) {
    /* Nothing to initialize for now */
}

void moving_average_filter(const signal_t *input, signal_t *output, size_t length, size_t window) {
    if (window > length) {
        window = length;
    }
    
    for (size_t i = 0; i < length; i++) {
        signal_t sum = 0.0f;
        size_t count = 0;
        
        /* Calculate average over window */
        for (size_t j = 0; j < window; j++) {
            if (i >= j) {
                sum += input[i - j];
                count++;
            }
        }
        
        output[i] = sum / count;
    }
}

signal_t calculate_baseline(const signal_t *signal, size_t length) {
    signal_t sum = 0.0f;
    size_t samples = (length < BASELINE_SAMPLES) ? length : BASELINE_SAMPLES;
    
    for (size_t i = 0; i < samples; i++) {
        sum += signal[i];
    }
    
    return sum / samples;
}

void remove_baseline(signal_t *signal, size_t length, signal_t baseline) {
    for (size_t i = 0; i < length; i++) {
        signal[i] -= baseline;
    }
}

void normalize_signal(signal_t *signal, size_t length) {
    /* Calculate mean */
    signal_t mean = 0.0f;
    for (size_t i = 0; i < length; i++) {
        mean += signal[i];
    }
    mean /= length;
    
    /* Remove mean (zero-center) */
    for (size_t i = 0; i < length; i++) {
        signal[i] -= mean;
    }
    
    /* Calculate standard deviation */
    signal_t variance = 0.0f;
    for (size_t i = 0; i < length; i++) {
        signal_t diff = signal[i];
        variance += diff * diff;
    }
    variance /= length;
    signal_t std_dev = sqrtf(variance);
    
    /* Normalize to unit variance (if std_dev is not zero) */
    if (std_dev > 0.001f) {
        for (size_t i = 0; i < length; i++) {
            signal[i] /= std_dev;
        }
    }
}

void bandpass_filter(const signal_t *input, signal_t *output, size_t length,
                     float low_freq, float high_freq) {
    /* Simple bandpass: apply moving average (low-pass) then high-pass */
    /* This is a simplified filter for demonstration */
    
    signal_t temp[WINDOW_SIZE];
    memcpy(temp, input, length * sizeof(signal_t));
    
    /* Low-pass component (moving average) */
    moving_average_filter(input, output, length, MA_FILTER_SIZE);
    
    /* High-pass component (subtract low-frequency from original) */
    for (size_t i = 0; i < length; i++) {
        output[i] = temp[i] - output[i];
    }
}

void preprocess_signal(signal_t *signal, size_t length) {
    /* Step 1: Calculate and remove baseline */
    signal_t baseline = calculate_baseline(signal, length);
    remove_baseline(signal, length, baseline);
    
    /* Step 2: Apply moving average filter for noise reduction */
    signal_t filtered[WINDOW_SIZE];
    moving_average_filter(signal, filtered, length, MA_FILTER_SIZE);
    memcpy(signal, filtered, length * sizeof(signal_t));
    
    /* Step 3: Normalize signal */
    normalize_signal(signal, length);
}
