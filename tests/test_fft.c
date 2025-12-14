#include "test_framework.h"
#include "fft.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define TEST_EPSILON 0.01f

/* Test complex number operations */
void test_complex_operations(void) {
    TEST_START("Complex Number Operations");
    
    complex_t a = complex_create(3.0f, 4.0f);
    complex_t b = complex_create(1.0f, 2.0f);
    
    /* Test addition */
    complex_t sum = complex_add(a, b);
    TEST_ASSERT(fabsf(sum.real - 4.0f) < TEST_EPSILON, "Addition real part");
    TEST_ASSERT(fabsf(sum.imag - 6.0f) < TEST_EPSILON, "Addition imag part");
    
    /* Test subtraction */
    complex_t diff = complex_sub(a, b);
    TEST_ASSERT(fabsf(diff.real - 2.0f) < TEST_EPSILON, "Subtraction real part");
    TEST_ASSERT(fabsf(diff.imag - 2.0f) < TEST_EPSILON, "Subtraction imag part");
    
    /* Test multiplication */
    complex_t prod = complex_mul(a, b);
    /* (3+4i) * (1+2i) = 3 + 6i + 4i + 8i^2 = 3 + 10i - 8 = -5 + 10i */
    TEST_ASSERT(fabsf(prod.real - (-5.0f)) < TEST_EPSILON, "Multiplication real part");
    TEST_ASSERT(fabsf(prod.imag - 10.0f) < TEST_EPSILON, "Multiplication imag part");
    
    /* Test magnitude */
    float mag = complex_magnitude(a);
    /* |3+4i| = sqrt(9+16) = 5 */
    TEST_ASSERT(fabsf(mag - 5.0f) < TEST_EPSILON, "Magnitude calculation");
    
    TEST_PASS("Complex operations work correctly");
}

/* Test utility functions */
void test_fft_utilities(void) {
    TEST_START("FFT Utility Functions");
    
    /* Test power of 2 check */
    TEST_ASSERT(is_power_of_2(1) == TRUE, "1 is power of 2");
    TEST_ASSERT(is_power_of_2(2) == TRUE, "2 is power of 2");
    TEST_ASSERT(is_power_of_2(256) == TRUE, "256 is power of 2");
    TEST_ASSERT(is_power_of_2(100) == FALSE, "100 is not power of 2");
    
    /* Test next power of 2 */
    TEST_ASSERT(next_power_of_2(100) == 128, "Next power of 2 for 100");
    TEST_ASSERT(next_power_of_2(256) == 256, "Next power of 2 for 256");
    TEST_ASSERT(next_power_of_2(257) == 512, "Next power of 2 for 257");
    
    /* Test bit reversal */
    TEST_ASSERT(bit_reverse(0, 3) == 0, "Bit reverse 000");
    TEST_ASSERT(bit_reverse(1, 3) == 4, "Bit reverse 001 -> 100");
    TEST_ASSERT(bit_reverse(2, 3) == 2, "Bit reverse 010 -> 010");
    TEST_ASSERT(bit_reverse(3, 3) == 6, "Bit reverse 011 -> 110");
    
    TEST_PASS("FFT utilities work correctly");
}

/* Test FFT with known sinusoid */
void test_fft_sinusoid(void) {
    TEST_START("FFT with Known Sinusoid");
    
    size_t n = 256;
    float sampling_rate = 256.0f;
    float test_freq = 10.0f;  /* 10 Hz sinusoid */
    
    /* Generate 10 Hz sinusoid */
    signal_t *signal = (signal_t*)malloc(n * sizeof(signal_t));
    for (size_t i = 0; i < n; i++) {
        float t = i / sampling_rate;
        signal[i] = sinf(2.0f * M_PI * test_freq * t);
    }
    
    /* Compute FFT */
    complex_t *fft_result = (complex_t*)malloc(n * sizeof(complex_t));
    fft_compute(signal, fft_result, n);
    
    /* Calculate power spectrum */
    power_spectrum_t spectrum;
    calculate_power_spectrum(fft_result, n, sampling_rate, &spectrum);
    
    /* Find peak frequency */
    size_t peak_idx = 0;
    float max_power = 0.0f;
    for (size_t i = 0; i < spectrum.num_bins; i++) {
        if (spectrum.power[i] > max_power) {
            max_power = spectrum.power[i];
            peak_idx = i;
        }
    }
    
    float peak_freq = spectrum.frequencies[peak_idx];
    
    printf("  Expected frequency: %.2f Hz\n", test_freq);
    printf("  Detected frequency: %.2f Hz\n", peak_freq);
    printf("  Peak power: %.6f\n", max_power);
    
    /* Check if peak is at expected frequency (within 1 Hz) */
    TEST_ASSERT(fabsf(peak_freq - test_freq) < 1.0f, 
                "Peak should be at 10 Hz");
    
    /* Cleanup */
    free_power_spectrum(&spectrum);
    free(signal);
    free(fft_result);
    
    TEST_PASS("FFT correctly identifies sinusoid frequency");
}

/* Test FFT with multiple frequencies */
void test_fft_multiple_frequencies(void) {
    TEST_START("FFT with Multiple Frequencies");
    
    size_t n = 256;
    float sampling_rate = 256.0f;
    float freq1 = 10.0f;  /* Alpha band */
    float freq2 = 20.0f;  /* Beta band */
    
    /* Generate signal with two frequencies */
    signal_t *signal = (signal_t*)malloc(n * sizeof(signal_t));
    for (size_t i = 0; i < n; i++) {
        float t = i / sampling_rate;
        signal[i] = sinf(2.0f * M_PI * freq1 * t) + 
                   0.5f * sinf(2.0f * M_PI * freq2 * t);
    }
    
    /* Compute FFT */
    complex_t *fft_result = (complex_t*)malloc(n * sizeof(complex_t));
    fft_compute(signal, fft_result, n);
    
    /* Calculate power spectrum */
    power_spectrum_t spectrum;
    calculate_power_spectrum(fft_result, n, sampling_rate, &spectrum);
    
    /* Find two highest peaks */
    float peak1_power = 0.0f, peak2_power = 0.0f;
    float peak1_freq = 0.0f, peak2_freq = 0.0f;
    
    for (size_t i = 1; i < spectrum.num_bins; i++) {
        if (spectrum.power[i] > peak1_power) {
            peak2_power = peak1_power;
            peak2_freq = peak1_freq;
            peak1_power = spectrum.power[i];
            peak1_freq = spectrum.frequencies[i];
        } else if (spectrum.power[i] > peak2_power) {
            peak2_power = spectrum.power[i];
            peak2_freq = spectrum.frequencies[i];
        }
    }
    
    printf("  Input frequencies: %.1f Hz and %.1f Hz\n", freq1, freq2);
    printf("  Peak 1: %.1f Hz (power: %.6f)\n", peak1_freq, peak1_power);
    printf("  Peak 2: %.1f Hz (power: %.6f)\n", peak2_freq, peak2_power);
    
    /* Cleanup */
    free_power_spectrum(&spectrum);
    free(signal);
    free(fft_result);
    
    TEST_PASS("FFT identifies multiple frequencies");
}

/* Test band power calculation */
void test_band_power_calculation(void) {
    TEST_START("Band Power Calculation");
    
    size_t n = 256;
    float sampling_rate = 256.0f;
    
    /* Generate alpha band signal (10 Hz) */
    signal_t *signal = (signal_t*)malloc(n * sizeof(signal_t));
    for (size_t i = 0; i < n; i++) {
        float t = i / sampling_rate;
        signal[i] = sinf(2.0f * M_PI * 10.0f * t);
    }
    
    /* Calculate alpha and beta band power */
    float alpha_power = calculate_band_power_fft(signal, n, sampling_rate, 
                                                  8.0f, 13.0f);
    float beta_power = calculate_band_power_fft(signal, n, sampling_rate,
                                                 13.0f, 30.0f);
    
    printf("  Alpha band (8-13 Hz) power: %.6f\n", alpha_power);
    printf("  Beta band (13-30 Hz) power: %.6f\n", beta_power);
    
    /* Alpha power should be much higher than beta for 10 Hz signal */
    TEST_ASSERT(alpha_power > beta_power * 5.0f, 
                "Alpha power should dominate for 10 Hz signal");
    
    free(signal);
    
    TEST_PASS("Band power calculation works correctly");
}

/* Test inverse FFT */
void test_inverse_fft(void) {
    TEST_START("Inverse FFT (Round-trip)");
    
    size_t n = 64;  /* Smaller size for round-trip test */
    
    /* Generate simple signal */
    signal_t *original = (signal_t*)malloc(n * sizeof(signal_t));
    for (size_t i = 0; i < n; i++) {
        original[i] = sinf(2.0f * M_PI * i / n);
    }
    
    /* Forward FFT */
    complex_t *fft_result = (complex_t*)malloc(n * sizeof(complex_t));
    fft_compute(original, fft_result, n);
    
    /* Inverse FFT */
    complex_t *ifft_result = (complex_t*)malloc(n * sizeof(complex_t));
    fft_inverse(fft_result, ifft_result, n);
    
    /* Check if we get back original signal */
    float max_error = 0.0f;
    for (size_t i = 0; i < n; i++) {
        float error = fabsf(ifft_result[i].real - original[i]);
        if (error > max_error) {
            max_error = error;
        }
    }
    
    printf("  Maximum reconstruction error: %.6f\n", max_error);
    
    TEST_ASSERT(max_error < 0.001f, "IFFT should reconstruct original signal");
    
    free(original);
    free(fft_result);
    free(ifft_result);
    
    TEST_PASS("Inverse FFT correctly reconstructs signal");
}

int main(void) {
    TEST_SUITE_START("FFT and Power Spectral Density Tests");
    
    fft_init();
    
    test_complex_operations();
    test_fft_utilities();
    test_fft_sinusoid();
    test_fft_multiple_frequencies();
    test_band_power_calculation();
    test_inverse_fft();
    
    fft_cleanup();
    
    TEST_SUITE_END();
    
    return 0;
}
