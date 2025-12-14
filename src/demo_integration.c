#include <stdio.h>
#include <stdlib.h>
#include "data_loader.h"
#include "fft.h"
#include "lda.h"
#include "feature_extraction.h"
#include "utils.h"

#define NUM_TRAIN_SAMPLES 50
#define NUM_TEST_SAMPLES 10

/*
 * INTEGRATION DEMO
 * 
 * This program demonstrates the Full BCI Pipeline:
 * 1. Data Loader: Loads EEG data from CSV files
 * 2. Preprocessing: (Simulated here as clean data)
 * 3. Feature Extraction: Uses FFT to get Alpha/Beta power
 * 4. Classification: Uses LDA to predict FOCUS vs RELAX
 */

/* Helper: Generate Sine Wave */
void generate_sine_wave(signal_t *buffer, size_t length, float freq, float sample_rate) {
    for (size_t i = 0; i < length; i++) {
        float t = (float)i / sample_rate;
        buffer[i] = sinf(2.0f * M_PI * freq * t);
    }
}

int main(void) {
    printf("\n=== BCI Project: Full Pipeline Integration Demo ===\n\n");
    
    /* 1. Initialize Modules */
    printf("[1] Initializing Modules...\n");
    
    /* Initialize with default config */
    data_config_t config;
    snprintf(config.data_directory, MAX_PATH_LENGTH, "data");
    snprintf(config.default_dataset, MAX_PATH_LENGTH, "sample_eeg_data.csv");
    config.auto_detect_format = TRUE;
    
    data_loader_init(&config);
    fft_init();
    
    lda_model_t lda_model;
    lda_init(&lda_model, 4); /* 4 features: Alpha, Beta, Variance, Skewness */
    
    printf("    ✓ Modules initialized\n\n");
    
    /* 2. Generate Training Data */
    printf("[2] Generating Training Data (Simulating loaded CSVs)...\n");
    
    lda_sample_t *samples = malloc(sizeof(lda_sample_t) * NUM_TRAIN_SAMPLES * 2);
    for (int i = 0; i < NUM_TRAIN_SAMPLES; i++) {
        signal_t signal_buffer[256];
        
        /* CLASS 0: RELAX (High Alpha - 10.5Hz) */
        generate_sine_wave(signal_buffer, 256, 10.5f, 256.0f);
        /* Apply same amplitude scaling as test data */
        for(int k=0; k<256; k++) signal_buffer[k] *= 200.0f;
        /* CRITICAL: Add same noise as test data for distribution match! */
        for(int k=0; k<256; k++) signal_buffer[k] += ((rand()%100)/10.0f);
        
        features_t feat_relax;
        extract_features(signal_buffer, 256, &feat_relax);
        
        samples[i].features = malloc(sizeof(signal_t) * 4);
        samples[i].features[0] = feat_relax.alpha_power;
        samples[i].features[1] = feat_relax.beta_power;
        samples[i].features[2] = feat_relax.variance;
        samples[i].features[3] = 0.0f;
        samples[i].label = 0; // RELAX
        
        /* CLASS 1: FOCUS (High Beta - 21.5Hz) */
        generate_sine_wave(signal_buffer, 256, 21.5f, 256.0f);
        /* Apply same amplitude scaling as test data */
        for(int k=0; k<256; k++) signal_buffer[k] *= 200.0f;
        /* CRITICAL: Add same noise as test data for distribution match! */
        for(int k=0; k<256; k++) signal_buffer[k] += ((rand()%100)/10.0f);
        
        features_t feat_focus;
        extract_features(signal_buffer, 256, &feat_focus);
        
        samples[NUM_TRAIN_SAMPLES + i].features = malloc(sizeof(signal_t) * 4);
        samples[NUM_TRAIN_SAMPLES + i].features[0] = feat_focus.alpha_power;
        samples[NUM_TRAIN_SAMPLES + i].features[1] = feat_focus.beta_power;
        samples[NUM_TRAIN_SAMPLES + i].features[2] = feat_focus.variance;
        samples[NUM_TRAIN_SAMPLES + i].features[3] = 0.0f;
        samples[NUM_TRAIN_SAMPLES + i].label = 1; // FOCUS
    }
    printf("    ✓ Generated %d training samples\n\n", NUM_TRAIN_SAMPLES * 2);
    
    /* 3. Train LDA Model */
    printf("[3] Training LDA Classifier...\n");
    lda_train(&lda_model, samples, NUM_TRAIN_SAMPLES * 2);
    printf("    ✓ Model trained. Threshold: %.4f\n\n", lda_model.threshold);
    
    /* Open CSV for logging */
    FILE *log_file = fopen("data/realtime_stream.csv", "w");
    if (log_file) {
        fprintf(log_file, "time,amplitude,alpha_power,beta_power,command,led_state\n");
    }

    /* 4. Process New "Real-time" Signals */
    printf("[4] Running Real-time Processing Loop...\n");
    printf("    (Simulating continuous EEG data windows)\n\n");
    
    signal_t dummy_signal[256]; /* Buffer for raw EEG */
    float current_time = 0.0f;
    
    /* Run for 500 iterations (~25 seconds of data at 50ms delay) */
    for (int iter = 0; iter < 500; iter++) {
        /* Determine simulated state based on time */
        /* 0-5s: FOCUS, 5-10s: RELAX, 10-15s: FOCUS... */
        float target_freq = (iter % 40 < 20) ? 20.0f : 10.0f; /* Switch every ~20 windows */
        command_t true_state = (target_freq == 20.0f) ? CMD_FOCUS : CMD_RELAX;
        
        /* A. Acquire Signal */
        generate_sine_wave(dummy_signal, 256, target_freq, 256.0f);
        
        /* Increase amplitude for visibility (simulate ~200uV signal) */
        for(int k=0; k<256; k++) dummy_signal[k] *= 200.0f;
        
        /* Add some noise */
        for(int k=0; k<256; k++) dummy_signal[k] += ((rand()%100)/10.0f);
        
        /* B. Feature Extraction (FFT) */
        features_t features;
        extract_features(dummy_signal, 256, &features);
        
        /* Prepare for LDA */
        signal_t input_features[4];
        input_features[0] = features.alpha_power;
        input_features[1] = features.beta_power;
        input_features[2] = features.variance;
        input_features[3] = 0.0f;
        
        /* C. Classification (LDA) */
        int prediction = lda_predict(&lda_model, input_features);
        
        /* Log data to CSV for Visualizer */
        if (log_file) {
             for (int s=0; s<256; s+=8) { 
                fprintf(log_file, "%.4f,%.4f,%.4f,%.4f,%s,%d\n", 
                        current_time + (float)s/256.0f, 
                        dummy_signal[s],
                        features.alpha_power, 
                        features.beta_power,
                        (prediction == 1) ? "FOCUS" : "RELAX",
                        (prediction == 1) ? 1 : 0);
             }
             fflush(log_file); 
        }
        current_time += 1.0f; 
        iter++;
        
        /* Print status every 10 iterations */
        if (iter % 10 == 0) {
            printf("    Window %d: Freq=%.1fHz -> Predicted: %s\n", 
                   iter, target_freq, (prediction == 1) ? "FOCUS" : "RELAX");
        }
        
        delay_ms(50); 
    }
    
    if (log_file) fclose(log_file);
    
    /* Cleanup */
    for(int i=0; i<NUM_TRAIN_SAMPLES*2; i++) free(samples[i].features);
    free(samples);
    lda_free(&lda_model);
    fft_cleanup();
    
    printf("=== Demo Complete ===\n");
    return 0;
}
