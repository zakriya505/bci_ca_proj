#include "classifier.h"
#include "utils.h"
#include <stdio.h>

void classifier_init(classifier_state_t *state) {
    state->last_command = CMD_NONE;
    state->debounce_counter = 0;
    state->baseline_amplitude = 1.0f;
}

void update_baseline(classifier_state_t *state, signal_t amplitude) {
    /* Exponential moving average for baseline */
    float alpha = 0.1f;
    state->baseline_amplitude = alpha * amplitude + (1.0f - alpha) * state->baseline_amplitude;
}

command_t classify_command(const features_t *features, classifier_state_t *state) {
    command_t detected_command = CMD_NONE;
    
    /* Priority 1: Check for blink artifact (highest priority) */
    if (features->peak_amplitude > BLINK_THRESHOLD * state->baseline_amplitude) {
        detected_command = CMD_BLINK;
    }
    /* Priority 2: Check for focus (high beta activity) */
    else if (features->beta_power > FOCUS_THRESHOLD) {
        detected_command = CMD_FOCUS;
    }
    /* Priority 3: Check for relax (high alpha activity) */
    else if (features->alpha_power > RELAX_THRESHOLD) {
        detected_command = CMD_RELAX;
    }
    
    /* Debouncing logic: require consistent detection */
    if (detected_command == state->last_command) {
        state->debounce_counter++;
    } else {
        state->debounce_counter = 1;
        state->last_command = detected_command;
    }
    
    /* Only return command if it's been stable for DEBOUNCE_COUNT samples */
    if (state->debounce_counter >= DEBOUNCE_COUNT) {
        /* Update baseline with current amplitude (if not a blink) */
        if (detected_command != CMD_BLINK) {
            update_baseline(state, features->peak_amplitude);
        }
        return detected_command;
    }
    
    return CMD_NONE;
}

const char* command_to_string(command_t cmd) {
    switch (cmd) {
        case CMD_FOCUS: return "FOCUS";
        case CMD_RELAX: return "RELAX";
        case CMD_BLINK: return "BLINK";
        case CMD_NONE:
        default:        return "NONE";
    }
}
