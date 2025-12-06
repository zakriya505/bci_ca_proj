#ifndef EEG_SIMULATOR_H
#define EEG_SIMULATOR_H

#include "types.h"
#include "config.h"

/* Initialize the EEG signal simulator */
void eeg_simulator_init(void);

/* Generate alpha wave (8-13 Hz) - associated with relaxation */
signal_t generate_alpha_wave(float time_sec, float frequency);

/* Generate beta wave (13-30 Hz) - associated with focus/concentration */
signal_t generate_beta_wave(float time_sec, float frequency);

/* Generate blink artifact - sharp spike in signal */
signal_t generate_blink_artifact(float time_sec, float blink_time);

/* Add Gaussian noise to signal */
signal_t add_noise(signal_t signal, float noise_level);

/* Generate a complete EEG signal sample for a given mental state */
void generate_eeg_sample(signal_t *buffer, size_t length, command_t state);

/* Generate mixed signal with multiple components */
signal_t generate_mixed_signal(float time_sec, float alpha_ratio, float beta_ratio, 
                                bool_t include_blink, float blink_time);

#endif /* EEG_SIMULATOR_H */
