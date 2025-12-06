#include "feature_extraction.h"
#include "utils.h"
#include <math.h>

void feature_extraction_init(void) {
    /* Nothing to initialize for now */
}

signal_t calculate_mean(const signal_t *signal, size_t length) {
    signal_t sum = 0.0f;
    for (size_t i = 0; i < length; i++) {
        sum += signal[i];
    }
    return sum / length;
}

signal_t calculate_variance(const signal_t *signal, size_t length) {
    signal_t mean = calculate_mean(signal, length);
    signal_t variance = 0.0f;
    
    for (size_t i = 0; i < length; i++) {
        signal_t diff = signal[i] - mean;
        variance += diff * diff;
    }
    
    return variance / length;
}

signal_t calculate_band_power(const signal_t *signal, size_t length,
                              float low_freq, float high_freq) {
    /* Simplified band power calculation */
    /* In a real implementation, this would use FFT */
    /* Here we approximate by calculating power in time domain */
    
    signal_t power = 0.0f;
    
    /* Calculate total power (sum of squares) */
    for (size_t i = 0; i < length; i++) {
        power += signal[i] * signal[i];
    }
    
    /* Normalize by length */
    power /= length;
    
    return power;
}

signal_t detect_peak_amplitude(const signal_t *signal, size_t length) {
    signal_t max_amplitude = 0.0f;
    
    for (size_t i = 0; i < length; i++) {
        signal_t abs_val = fabsf(signal[i]);
        if (abs_val > max_amplitude) {
            max_amplitude = abs_val;
        }
    }
    
    return max_amplitude;
}

void extract_features(const signal_t *signal, size_t length, features_t *features) {
    /* Extract alpha band power (8-13 Hz) */
    features->alpha_power = calculate_band_power(signal, length, 
                                                 ALPHA_LOW_FREQ, ALPHA_HIGH_FREQ);
    
    /* Extract beta band power (13-30 Hz) */
    features->beta_power = calculate_band_power(signal, length,
                                                BETA_LOW_FREQ, BETA_HIGH_FREQ);
    
    /* Detect peak amplitude for blink detection */
    features->peak_amplitude = detect_peak_amplitude(signal, length);
    
    /* Calculate signal variance */
    features->variance = calculate_variance(signal, length);
    
    /* Normalize powers to get relative ratios */
    signal_t total_power = features->alpha_power + features->beta_power;
    if (total_power > 0.001f) {
        features->alpha_power /= total_power;
        features->beta_power /= total_power;
    }
}
