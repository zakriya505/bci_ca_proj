#ifndef FFT_H
#define FFT_H

#include "types.h"
#include "config.h"
#include <math.h>

/* Complex number type for FFT */
typedef struct {
    float real;
    float imag;
} complex_t;

/* FFT configuration */
typedef struct {
    size_t fft_size;           /* FFT size (must be power of 2) */
    float sampling_rate;       /* Sampling rate in Hz */
    bool_t use_window;         /* Apply Hanning window */
} fft_config_t;

/* Power spectrum result */
typedef struct {
    float *power;              /* Power at each frequency bin */
    float *frequencies;        /* Frequency values for each bin */
    size_t num_bins;           /* Number of frequency bins */
    float frequency_resolution;/* Frequency resolution (Hz per bin) */
} power_spectrum_t;

/* ========== Complex Number Operations ========== */

/* Create complex number */
complex_t complex_create(float real, float imag);

/* Add two complex numbers */
complex_t complex_add(complex_t a, complex_t b);

/* Subtract two complex numbers */
complex_t complex_sub(complex_t a, complex_t b);

/* Multiply two complex numbers */
complex_t complex_mul(complex_t a, complex_t b);

/* Calculate magnitude of complex number */
float complex_magnitude(complex_t c);

/* Calculate squared magnitude (for power) */
float complex_magnitude_squared(complex_t c);

/* ========== FFT Functions ========== */

/* Initialize FFT module */
void fft_init(void);

/* Check if number is power of 2 */
bool_t is_power_of_2(size_t n);

/* Find next power of 2 >= n */
size_t next_power_of_2(size_t n);

/* Bit reversal for FFT */
size_t bit_reverse(size_t n, size_t bits);

/* Apply Hanning window to signal */
void apply_hanning_window(signal_t *signal, size_t length);

/* Cooley-Tukey FFT algorithm (radix-2, decimation-in-time)
 * input: Real signal array
 * output: Complex FFT result
 * n: Size of input (must be power of 2)
 */
void fft_compute(const signal_t *input, complex_t *output, size_t n);

/* Inverse FFT */
void fft_inverse(const complex_t *input, complex_t *output, size_t n);

/* ========== Power Spectral Density ========== */

/* Calculate power spectrum from FFT result
 * fft_result: Complex FFT output
 * n: FFT size
 * sampling_rate: Sampling rate in Hz
 * spectrum: Output power spectrum structure
 */
void calculate_power_spectrum(const complex_t *fft_result, size_t n,
                              float sampling_rate, power_spectrum_t *spectrum);

/* Calculate power in specific frequency band using PSD
 * spectrum: Power spectrum from calculate_power_spectrum
 * low_freq: Lower frequency bound (Hz)
 * high_freq: Upper frequency bound (Hz)
 * Returns: Total power in the frequency band
 */
float calculate_band_power_psd(const power_spectrum_t *spectrum,
                               float low_freq, float high_freq);

/* Convenience function: Calculate band power directly from signal
 * signal: Input signal
 * length: Signal length
 * sampling_rate: Sampling rate in Hz
 * low_freq: Lower frequency bound
 * high_freq: Upper frequency bound
 */
float calculate_band_power_fft(const signal_t *signal, size_t length,
                               float sampling_rate, float low_freq, float high_freq);

/* Free power spectrum memory */
void free_power_spectrum(power_spectrum_t *spectrum);

/* ========== Utility Functions ========== */

/* Calculate frequency resolution */
float get_frequency_resolution(size_t fft_size, float sampling_rate);

/* Get frequency bin index for given frequency */
size_t get_frequency_bin(float frequency, float sampling_rate, size_t fft_size);

/* Cleanup FFT module */
void fft_cleanup(void);

#endif /* FFT_H */
