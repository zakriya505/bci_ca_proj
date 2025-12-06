#include "eeg_simulator.h"
#include "utils.h"
#include <math.h>
#include <stdlib.h>
#include <time.h>

static int simulator_initialized = 0;

void eeg_simulator_init(void) {
    if (!simulator_initialized) {
        seed_random((unsigned int)time(NULL));
        simulator_initialized = 1;
    }
}

signal_t generate_alpha_wave(float time_sec, float frequency) {
    /* Alpha waves: 8-13 Hz, associated with relaxed, wakeful state */
    return ALPHA_AMPLITUDE * sinf(2.0f * M_PI * frequency * time_sec);
}

signal_t generate_beta_wave(float time_sec, float frequency) {
    /* Beta waves: 13-30 Hz, associated with active thinking and focus */
    return BETA_AMPLITUDE * sinf(2.0f * M_PI * frequency * time_sec);
}

signal_t generate_blink_artifact(float time_sec, float blink_time) {
    /* Blink creates a sharp spike lasting ~200ms */
    float time_diff = time_sec - blink_time;
    
    if (time_diff < 0.0f || time_diff > 0.2f) {
        return 0.0f;
    }
    
    /* Gaussian-like pulse */
    float sigma = 0.05f;
    float exponent = -(time_diff * time_diff) / (2.0f * sigma * sigma);
    return BLINK_AMPLITUDE * expf(exponent);
}

signal_t add_noise(signal_t signal, float noise_level) {
    /* Add Gaussian-like noise */
    float noise = random_float(-noise_level, noise_level);
    return signal + noise;
}

signal_t generate_mixed_signal(float time_sec, float alpha_ratio, float beta_ratio,
                                bool_t include_blink, float blink_time) {
    signal_t signal = 0.0f;
    
    /* Mix alpha waves (use middle of alpha band: 10.5 Hz) */
    if (alpha_ratio > 0.0f) {
        signal += alpha_ratio * generate_alpha_wave(time_sec, 10.5f);
    }
    
    /* Mix beta waves (use middle of beta band: 21.5 Hz) */
    if (beta_ratio > 0.0f) {
        signal += beta_ratio * generate_beta_wave(time_sec, 21.5f);
    }
    
    /* Add blink artifact if needed */
    if (include_blink) {
        signal += generate_blink_artifact(time_sec, blink_time);
    }
    
    /* Add background noise */
    signal = add_noise(signal, NOISE_LEVEL);
    
    return signal;
}

void generate_eeg_sample(signal_t *buffer, size_t length, command_t state) {
    float dt = 1.0f / SAMPLING_RATE;
    float alpha_ratio = 0.0f;
    float beta_ratio = 0.0f;
    bool_t include_blink = FALSE;
    float blink_time = 0.5f;
    
    /* Configure signal based on desired mental state */
    switch (state) {
        case CMD_FOCUS:
            /* High beta, low alpha */
            beta_ratio = 1.0f;
            alpha_ratio = 0.3f;
            break;
            
        case CMD_RELAX:
            /* High alpha, low beta */
            alpha_ratio = 1.0f;
            beta_ratio = 0.3f;
            break;
            
        case CMD_BLINK:
            /* Normal background with blink artifact */
            alpha_ratio = 0.5f;
            beta_ratio = 0.5f;
            include_blink = TRUE;
            break;
            
        case CMD_NONE:
        default:
            /* Balanced background activity */
            alpha_ratio = 0.5f;
            beta_ratio = 0.5f;
            break;
    }
    
    /* Generate signal samples */
    for (size_t i = 0; i < length; i++) {
        float time_sec = i * dt;
        buffer[i] = generate_mixed_signal(time_sec, alpha_ratio, beta_ratio,
                                          include_blink, blink_time);
    }
}
