#include "test_framework.h"
#include "../include/types.h"
#include "../include/config.h"
#include "../include/feature_extraction.h"
#include <math.h>

/* Test band power calculation with alpha-dominant signal */
void test_alpha_band_power() {
    TEST_START("Alpha Band Power Calculation");
    
    signal_t signal[256];
    
    /* Generate alpha wave (10 Hz) */
    for (int i = 0; i < 256; i++) {
        float t = i / 256.0f;
        signal[i] = 50.0f * sinf(2.0f * M_PI * 10.0f * t);
    }
    
    signal_t alpha_power = calculate_band_power(signal, 256, ALPHA_LOW_FREQ, ALPHA_HIGH_FREQ);
    signal_t beta_power = calculate_band_power(signal, 256, BETA_LOW_FREQ, BETA_HIGH_FREQ);
    
    /* Alpha should be significantly higher than beta for this signal */
    ASSERT_TRUE(alpha_power > beta_power, "Alpha power > Beta power for 10Hz signal");
    ASSERT_TRUE(alpha_power > 0.0f, "Alpha power is positive");
}

/* Test band power calculation with beta-dominant signal */
void test_beta_band_power() {
    TEST_START("Beta Band Power Calculation");
    
    signal_t signal[256];
    
    /* Generate beta wave (21.5 Hz) */
    for (int i = 0; i < 256; i++) {
        float t = i / 256.0f;
        signal[i] = 30.0f * sinf(2.0f * M_PI * 21.5f * t);
    }
    
    signal_t alpha_power = calculate_band_power(signal, 256, ALPHA_LOW_FREQ, ALPHA_HIGH_FREQ);
    signal_t beta_power = calculate_band_power(signal, 256, BETA_LOW_FREQ, BETA_HIGH_FREQ);
    
    /* Beta should be significantly higher than alpha for this signal */
    ASSERT_TRUE(beta_power > alpha_power, "Beta power > Alpha power for 21.5Hz signal");
    ASSERT_TRUE(beta_power > 0.0f, "Beta power is positive");
}

/* Test feature extraction normalization */
void test_feature_normalization() {
    TEST_START("Feature Normalization");
    
    signal_t signal[256];
    
    /* Generate mixed signal */
    for (int i = 0; i < 256; i++) {
        float t = i / 256.0f;
        signal[i] = 50.0f * sinf(2.0f * M_PI * 10.0f * t) + 
                   30.0f * sinf(2.0f * M_PI * 21.5f * t);
    }
    
    features_t features;
    extract_features(signal, 256, &features);
    
    /* After normalization, alpha + beta should be close to 1.0 */
    float sum = features.alpha_power + features.beta_power;
    ASSERT_FLOAT_EQUAL(1.0f, sum, 0.001f, "Normalized powers sum to 1.0");
    
    /* Both should be between 0 and 1 */
    ASSERT_TRUE(features.alpha_power >= 0.0f && features.alpha_power <= 1.0f, 
                "Alpha power in range [0, 1]");
    ASSERT_TRUE(features.beta_power >= 0.0f && features.beta_power <= 1.0f, 
                "Beta power in range [0, 1]");
}

/* Test peak amplitude detection */
void test_peak_amplitude() {
    TEST_START("Peak Amplitude Detection");
    
    signal_t signal[256];
    
    /* Generate signal with known peak */
    for (int i = 0; i < 256; i++) {
        signal[i] = 10.0f * sinf(2.0f * M_PI * 10.0f * i / 256.0f);
    }
    
    /* Add a large spike */
    signal[128] = 200.0f;
    
    signal_t peak = detect_peak_amplitude(signal, 256);
    
    ASSERT_FLOAT_EQUAL(200.0f, peak, 1.0f, "Peak amplitude correctly detected");
}

/* Test variance calculation */
void test_variance_calculation() {
    TEST_START("Variance Calculation");
    
    signal_t signal[10] = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f, 9.0f, 10.0f};
    
    signal_t mean = calculate_mean(signal, 10);
    ASSERT_FLOAT_EQUAL(5.5f, mean, 0.01f, "Mean calculation correct");
    
    signal_t variance = calculate_variance(signal, 10);
    /* Expected variance = 8.25 */
    ASSERT_FLOAT_EQUAL(8.25f, variance, 0.1f, "Variance calculation correct");
}

/* Test edge case: zero signal */
void test_zero_signal() {
    TEST_START("Zero Signal Edge Case");
    
    signal_t signal[256] = {0};
    features_t features;
    
    extract_features(signal, 256, &features);
    
    /* Should handle zero signal gracefully */
    ASSERT_FLOAT_EQUAL(0.5f, features.alpha_power, 0.01f, 
                      "Zero signal: alpha power defaults to 0.5");
    ASSERT_FLOAT_EQUAL(0.5f, features.beta_power, 0.01f, 
                      "Zero signal: beta power defaults to 0.5");
}

int main() {
    TEST_SUITE_START("Feature Extraction Tests");
    
    /* Initialize feature extraction */
    feature_extraction_init();
    
    /* Run tests */
    test_alpha_band_power();
    test_beta_band_power();
    test_feature_normalization();
    test_peak_amplitude();
    test_variance_calculation();
    test_zero_signal();
    
    TEST_SUITE_END();
    
    return tests_failed > 0 ? 1 : 0;
}
