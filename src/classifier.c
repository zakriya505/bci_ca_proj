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

void predict_impairments(const features_t *features, predictions_t *predictions) {
    /* Visual Impairment Detection
     * Based on alpha power in occipital lobe
     * Low alpha during relaxed states indicates visual processing issues
     */
    if (features->alpha_power >= VISUAL_ALPHA_NORMAL) {
        predictions->visual_impairment = PRED_NORMAL;
    } else if (features->alpha_power >= VISUAL_ALPHA_BORDERLINE) {
        predictions->visual_impairment = PRED_BORDERLINE;
    } else {
        predictions->visual_impairment = PRED_IMPAIRED;
    }
    
    /* Motor Impairment Detection
     * Based on beta/mu rhythm in motor cortex
     * Abnormal beta power indicates motor control issues
     */
    if (features->beta_power >= MOTOR_BETA_NORMAL) {
        predictions->motor_impairment = PRED_NORMAL;
    } else if (features->beta_power >= MOTOR_BETA_BORDERLINE) {
        predictions->motor_impairment = PRED_BORDERLINE;
    } else {
        predictions->motor_impairment = PRED_IMPAIRED;
    }
    
    /* Attention Deficit Detection
     * Based on theta/beta ratio in frontal lobe
     * High theta/beta ratio indicates attention problems
     */
    signal_t theta_beta_ratio = 0.0f;
    if (features->beta_power > 0.01f) {
        theta_beta_ratio = features->theta_power / features->beta_power;
    } else {
        theta_beta_ratio = 10.0f;  /* Very high ratio if beta is negligible */
    }
    
    if (theta_beta_ratio <= ATTENTION_RATIO_NORMAL) {
        predictions->attention_deficit = PRED_NORMAL;
    } else if (theta_beta_ratio <= ATTENTION_RATIO_BORDER) {
        predictions->attention_deficit = PRED_BORDERLINE;
    } else {
        predictions->attention_deficit = PRED_IMPAIRED;
    }
}

const char* prediction_to_string(prediction_t pred) {
    switch (pred) {
        case PRED_NORMAL:     return "NORMAL";
        case PRED_BORDERLINE: return "BORDERLINE";
        case PRED_IMPAIRED:   return "IMPAIRED";
        default:              return "UNKNOWN";
    }
}
