#ifndef FEATURE_EXTRACTION_H
#define FEATURE_EXTRACTION_H

#include "types.h"
#include "config.h"

/* Initialize feature extraction module */
void feature_extraction_init(void);

/* Calculate power in a specific frequency band */
signal_t calculate_band_power(const signal_t *signal, size_t length, 
                              float low_freq, float high_freq);

/* Calculate signal variance */
signal_t calculate_variance(const signal_t *signal, size_t length);

/* Detect peak amplitude (for blink detection) */
signal_t detect_peak_amplitude(const signal_t *signal, size_t length);

/* Calculate mean of signal */
signal_t calculate_mean(const signal_t *signal, size_t length);

/* Extract all features from preprocessed signal */
void extract_features(const signal_t *signal, size_t length, features_t *features);

/* Assembly-optimized power calculation (implemented in feature_extraction_asm.S) */
extern signal_t calculate_power_asm(const signal_t *signal, size_t length);

/* Assembly-optimized variance calculation */
extern signal_t calculate_variance_asm(const signal_t *signal, size_t length, signal_t mean);

#endif /* FEATURE_EXTRACTION_H */
