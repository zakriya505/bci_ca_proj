#ifndef CLASSIFIER_H
#define CLASSIFIER_H

#include "types.h"
#include "config.h"

/* Classifier state for debouncing */
typedef struct {
    command_t last_command;
    int debounce_counter;
    signal_t baseline_amplitude;
} classifier_state_t;

/* Initialize classifier */
void classifier_init(classifier_state_t *state);

/* Classify mental command based on extracted features */
command_t classify_command(const features_t *features, classifier_state_t *state);

/* Get string representation of command */
const char* command_to_string(command_t cmd);

/* Update classifier baseline */
void update_baseline(classifier_state_t *state, signal_t amplitude);

/* Predict health impairments based on EEG features */
void predict_impairments(const features_t *features, predictions_t *predictions);

/* Get string representation of prediction */
const char* prediction_to_string(prediction_t pred);

#endif /* CLASSIFIER_H */
