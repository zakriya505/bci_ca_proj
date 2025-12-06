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

#endif /* CLASSIFIER_H */
