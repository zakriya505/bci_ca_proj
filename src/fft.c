#include "fft.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ========== Complex Number Operations ========== */

complex_t complex_create(float real, float imag) {
    complex_t c;
    c.real = real;
    c.imag = imag;
    return c;
}

complex_t complex_add(complex_t a, complex_t b) {
    complex_t result;
    result.real = a.real + b.real;
    result.imag = a.imag + b.imag;
    return result;
}

complex_t complex_sub(complex_t a, complex_t b) {
    complex_t result;
    result.real = a.real - b.real;
    result.imag = a.imag - b.imag;
    return result;
}

complex_t complex_mul(complex_t a, complex_t b) {
    complex_t result;
    /* (a + bi) * (c + di) = (ac - bd) + (ad + bc)i */
    result.real = a.real * b.real - a.imag * b.imag;
    result.imag = a.real * b.imag + a.imag * b.real;
    return result;
}

float complex_magnitude(complex_t c) {
    return sqrtf(c.real * c.real + c.imag * c.imag);
}

float complex_magnitude_squared(complex_t c) {
    return c.real * c.real + c.imag * c.imag;
}

/* ========== FFT Utility Functions ========== */

void fft_init(void) {
    /* Nothing to initialize for now */
}

bool_t is_power_of_2(size_t n) {
    return n > 0 && (n & (n - 1)) == 0;
}

size_t next_power_of_2(size_t n) {
    if (n == 0) return 1;
    
    n--;
    n |= n >> 1;
    n |= n >> 2;
    n |= n >> 4;
    n |= n >> 8;
    n |= n >> 16;
    n++;
    
    return n;
}

size_t bit_reverse(size_t n, size_t bits) {
    size_t reversed = 0;
    for (size_t i = 0; i < bits; i++) {
        if (n & (1 << i)) {
            reversed |= 1 << (bits - 1 - i);
        }
    }
    return reversed;
}

void apply_hanning_window(signal_t *signal, size_t length) {
    for (size_t i = 0; i < length; i++) {
        float window = 0.5f * (1.0f - cosf(2.0f * M_PI * i / (length - 1)));
        signal[i] *= window;
    }
}

/* ========== FFT Algorithm ========== */

/* Cooley-Tukey FFT (radix-2, decimation-in-time) */
void fft_compute(const signal_t *input, complex_t *output, size_t n) {
    if (!is_power_of_2(n)) {
        log_error("FFT size must be power of 2, got %zu", n);
        return;
    }
    
    /* Calculate number of bits */
    size_t bits = 0;
    size_t temp = n;
    while (temp > 1) {
        bits++;
        temp >>= 1;
    }
    
    /* Bit-reversal permutation */
    for (size_t i = 0; i < n; i++) {
        size_t j = bit_reverse(i, bits);
        output[j].real = input[i];
        output[j].imag = 0.0f;
    }
    
    /* Cooley-Tukey FFT algorithm */
    for (size_t stage = 1; stage <= bits; stage++) {
        size_t m = 1 << stage;           /* Size of sub-DFT */
        size_t m2 = m >> 1;              /* Half size */
        
        /* Twiddle factor exp(-2*pi*i/m) */
        float angle = -2.0f * M_PI / m;
        complex_t wm = complex_create(cosf(angle), sinf(angle));
        
        for (size_t k = 0; k < n; k += m) {
            complex_t w = complex_create(1.0f, 0.0f);
            
            for (size_t j = 0; j < m2; j++) {
                /* Butterfly operation */
                complex_t t = complex_mul(w, output[k + j + m2]);
                complex_t u = output[k + j];
                
                output[k + j] = complex_add(u, t);
                output[k + j + m2] = complex_sub(u, t);
                
                w = complex_mul(w, wm);
            }
        }
    }
}

void fft_inverse(const complex_t *input, complex_t *output, size_t n) {
    if (!is_power_of_2(n)) {
        log_error("IFFT size must be power of 2, got %zu", n);
        return;
    }
    
    /* Calculate number of bits */
    size_t bits = 0;
    size_t temp = n;
    while (temp > 1) {
        bits++;
        temp >>= 1;
    }
    
    /* Bit-reversal permutation with complex conjugate */
    for (size_t i = 0; i < n; i++) {
        size_t j = bit_reverse(i, bits);
        output[j].real = input[i].real;
        output[j].imag = -input[i].imag;  /* Conjugate */
    }
    
    /* FFT algorithm (same as forward, but with conjugated input) */
    for (size_t stage = 1; stage <= bits; stage++) {
        size_t m = 1 << stage;
        size_t m2 = m >> 1;
        
        float angle = -2.0f * M_PI / m;
        complex_t wm = complex_create(cosf(angle), sinf(angle));
        
        for (size_t k = 0; k < n; k += m) {
            complex_t w = complex_create(1.0f, 0.0f);
            
            for (size_t j = 0; j < m2; j++) {
                complex_t t = complex_mul(w, output[k + j + m2]);
                complex_t u = output[k + j];
                
                output[k + j] = complex_add(u, t);
                output[k + j + m2] = complex_sub(u, t);
                
                w = complex_mul(w, wm);
            }
        }
    }
    
    /* Scale and take conjugate for IFFT */
    float scale = 1.0f / n;
    for (size_t i = 0; i < n; i++) {
        output[i].real *= scale;
        output[i].imag *= -scale;  /* Conjugate */
    }
}

/* ========== Power Spectral Density ========== */

void calculate_power_spectrum(const complex_t *fft_result, size_t n,
                              float sampling_rate, power_spectrum_t *spectrum) {
    if (spectrum == NULL) return;
    
    /* Number of unique frequency bins (0 to Nyquist) */
    spectrum->num_bins = n / 2 + 1;
    spectrum->frequency_resolution = sampling_rate / n;
    
    /* Allocate memory for power and frequencies */
    spectrum->power = (float*)malloc(spectrum->num_bins * sizeof(float));
    spectrum->frequencies = (float*)malloc(spectrum->num_bins * sizeof(float));
    
    if (spectrum->power == NULL || spectrum->frequencies == NULL) {
        log_error("Failed to allocate memory for power spectrum");
        return;
    }
    
    /* Calculate power and frequencies for each bin */
    for (size_t i = 0; i < spectrum->num_bins; i++) {
        /* Frequency for this bin */
        spectrum->frequencies[i] = i * spectrum->frequency_resolution;
        
        /* Power = |FFT[k]|^2 / n^2 */
        /* Multiply DC and Nyquist by 1, others by 2 (since we only keep half) */
        float magnitude_sq = complex_magnitude_squared(fft_result[i]);
        
        if (i == 0 || i == n/2) {
            spectrum->power[i] = magnitude_sq / (n * n);
        } else {
            spectrum->power[i] = 2.0f * magnitude_sq / (n * n);
        }
    }
}

float calculate_band_power_psd(const power_spectrum_t *spectrum,
                               float low_freq, float high_freq) {
    if (spectrum == NULL || spectrum->power == NULL) {
        return 0.0f;
    }
    
    float total_power = 0.0f;
    
    /* Sum power in the frequency band */
    for (size_t i = 0; i < spectrum->num_bins; i++) {
        float freq = spectrum->frequencies[i];
        if (freq >= low_freq && freq <= high_freq) {
            total_power += spectrum->power[i];
        }
    }
    
    /* Multiply by frequency resolution to get power (integrate) */
    total_power *= spectrum->frequency_resolution;
    
    return total_power;
}

float calculate_band_power_fft(const signal_t *signal, size_t length,
                               float sampling_rate, float low_freq, float high_freq) {
    /* Ensure FFT size is power of 2 */
    size_t fft_size = next_power_of_2(length);
    
    /* Allocate buffers */
    signal_t *padded_signal = (signal_t*)calloc(fft_size, sizeof(signal_t));
    complex_t *fft_result = (complex_t*)malloc(fft_size * sizeof(complex_t));
    
    if (padded_signal == NULL || fft_result == NULL) {
        log_error("Failed to allocate FFT buffers");
        free(padded_signal);
        free(fft_result);
        return 0.0f;
    }
    
    /* Copy signal and zero-pad */
    memcpy(padded_signal, signal, length * sizeof(signal_t));
    
    /* Apply Hanning window to reduce spectral leakage */
    apply_hanning_window(padded_signal, length);
    
    /* Compute FFT */
    fft_compute(padded_signal, fft_result, fft_size);
    
    /* Calculate power spectrum */
    power_spectrum_t spectrum;
    calculate_power_spectrum(fft_result, fft_size, sampling_rate, &spectrum);
    
    /* Get band power */
    float band_power = calculate_band_power_psd(&spectrum, low_freq, high_freq);
    
    /* Cleanup */
    free_power_spectrum(&spectrum);
    free(padded_signal);
    free(fft_result);
    
    return band_power;
}

void free_power_spectrum(power_spectrum_t *spectrum) {
    if (spectrum != NULL) {
        if (spectrum->power != NULL) {
            free(spectrum->power);
            spectrum->power = NULL;
        }
        if (spectrum->frequencies != NULL) {
            free(spectrum->frequencies);
            spectrum->frequencies = NULL;
        }
        spectrum->num_bins = 0;
    }
}

/* ========== Utility Functions ========== */

float get_frequency_resolution(size_t fft_size, float sampling_rate) {
    return sampling_rate / fft_size;
}

size_t get_frequency_bin(float frequency, float sampling_rate, size_t fft_size) {
    float freq_res = get_frequency_resolution(fft_size, sampling_rate);
    return (size_t)(frequency / freq_res + 0.5f);
}

void fft_cleanup(void) {
    /* Nothing to cleanup for now */
}
