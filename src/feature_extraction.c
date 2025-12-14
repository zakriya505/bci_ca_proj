#include "feature_extraction.h"
#include "fft.h"
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

signal_t calculate_skewness(const signal_t *signal, size_t length) {
    /* Skewness: measure of asymmetry of the signal distribution */
    /* skewness = E[(X - μ)³] / σ³ */
    
    signal_t mean = calculate_mean(signal, length);
    signal_t variance = calculate_variance(signal, length);
    signal_t std_dev = sqrtf(variance);
    
    /* Avoid division by zero */
    if (std_dev < 0.001f) {
        return 0.0f;
    }
    
    signal_t skewness = 0.0f;
    for (size_t i = 0; i < length; i++) {
        signal_t diff = signal[i] - mean;
        signal_t normalized = diff / std_dev;
        skewness += normalized * normalized * normalized;
    }
    
    return skewness / length;
}

signal_t calculate_band_power(const signal_t *signal, size_t length,
                              float low_freq, float high_freq) {
    /* Use FFT-based Power Spectral Density for accurate band power */
    #ifdef USE_FFT_BANDPOWER
        /* Use FFT for accurate frequency analysis */
        return calculate_band_power_fft(signal, length, SAMPLING_RATE, 
                                       low_freq, high_freq);
    #else
        /* Fallback: simplified approximation (faster but less accurate) */
        /* This uses a simplified approach: estimate power contribution from frequency band */
        
        signal_t power = 0.0f;
        
        /* Center frequency of the band */
        float center_freq = (low_freq + high_freq) / 2.0f;
        
        /* Calculate power weighted by frequency content */
        signal_t weighted_power = 0.0f;
        
        if (center_freq < 15.0f) {
            /* Alpha band - favor smoother signals */
            for (size_t i = 0; i < length; i++) {
                weighted_power += signal[i] * signal[i];
            }
            /* Penalize rapid changes (high frequency content) */
            for (size_t i = 1; i < length; i++) {
                signal_t diff = signal[i] - signal[i-1];
                weighted_power -= fabsf(diff) * 0.5f;
            }
        } else {
            /* Beta band - favor faster oscillations */
            for (size_t i = 0; i < length; i++) {
                weighted_power += signal[i] * signal[i];
            }
            /* Reward rapid changes (high frequency content) */
            for (size_t i = 1; i < length; i++) {
                signal_t diff = signal[i] - signal[i-1];
                weighted_power += fabsf(diff) * 0.4f;
            }
        }
        
        /* Normalize by length */
        power = weighted_power / length;
        
        /* Ensure non-negative */
        if (power < 0.0f) power = 0.0f;
        
        return power;
    #endif
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
    if (total_power > 0.01f) {  /* Increased threshold for more robust error handling */
        features->alpha_power /= total_power;
        features->beta_power /= total_power;
    } else {
        /* No significant power detected, set to neutral values */
        features->alpha_power = 0.5f;
        features->beta_power = 0.5f;
    }
}
