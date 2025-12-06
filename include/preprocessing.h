#ifndef PREPROCESSING_H
#define PREPROCESSING_H

#include "types.h"
#include "config.h"

/* Initialize preprocessing module */
void preprocessing_init(void);

/* Apply moving average filter to reduce noise */
void moving_average_filter(const signal_t *input, signal_t *output, size_t length, size_t window);

/* Normalize signal to zero mean */
void normalize_signal(signal_t *signal, size_t length);

/* Calculate baseline (DC offset) of signal */
signal_t calculate_baseline(const signal_t *signal, size_t length);

/* Remove baseline from signal */
void remove_baseline(signal_t *signal, size_t length, signal_t baseline);

/* Simple band-pass filter (alpha or beta band) */
void bandpass_filter(const signal_t *input, signal_t *output, size_t length, 
                     float low_freq, float high_freq);

/* Complete preprocessing pipeline */
void preprocess_signal(signal_t *signal, size_t length);

/* Assembly-optimized moving average (implemented in preprocessing_asm.S) */
extern void moving_average_asm(const signal_t *input, signal_t *output, 
                               size_t length, size_t window);

#endif /* PREPROCESSING_H */
