#include "test_framework.h"
#include "../include/types.h"
#include "../include/config.h"
#include "../include/classifier.h"

/* Test FOCUS command detection */
void test_focus_detection() {
    TEST_START("FOCUS Command Detection");
    
    classifier_state_t state;
    classifier_init(&state);
    
    features_t features;
    features.alpha_power = 0.3f;  /* Low alpha */
    features.beta_power = 0.7f;   /* High beta (> 0.6 threshold) */
    features.peak_amplitude = 2.0f;  /* Normal amplitude - won't trigger blink */
    features.variance = 100.0f;
    
    /* First detection should require debouncing */
    command_t cmd1 = classify_command(&features, &state);
    ASSERT_EQUAL(CMD_NONE, cmd1, "First detection returns NONE (debouncing)");
    
    /* Second detection - triggers with DEBOUNCE_COUNT=2 */
    command_t cmd2 = classify_command(&features, &state);
    ASSERT_EQUAL(CMD_FOCUS, cmd2, "Second detection returns FOCUS (debounce threshold met)");
    
    /* Third detection - still FOCUS */
    command_t cmd3 = classify_command(&features, &state);
    ASSERT_EQUAL(CMD_FOCUS, cmd3, "Third detection returns FOCUS");
}

/* Test RELAX command detection */
void test_relax_detection() {
    TEST_START("RELAX Command Detection");
    
    classifier_state_t state;
    classifier_init(&state);
    
    features_t features;
    features.alpha_power = 0.7f;  /* High alpha (> 0.6 threshold) */
    features.beta_power = 0.3f;   /* Low beta */
    features.peak_amplitude = 2.0f;  /* Normal amplitude - won't trigger blink */
    features.variance = 100.0f;
    
    /* Debounce and detect - triggers on 2nd call with DEBOUNCE_COUNT=2 */
    classify_command(&features, &state);
    command_t cmd = classify_command(&features, &state);
    
    ASSERT_EQUAL(CMD_RELAX, cmd, "RELAX command detected");
}

/* Test BLINK command detection (highest priority) */
void test_blink_detection() {
    TEST_START("BLINK Command Detection");
    
    classifier_state_t state;
    classifier_init(&state);
    
    features_t features;
    features.alpha_power = 0.5f;
    features.beta_power = 0.5f;
    features.peak_amplitude = 500.0f;  /* Very high amplitude */
    features.variance = 10000.0f;
    
    /* Blink should be detected after debouncing */
    classify_command(&features, &state);
    command_t cmd = classify_command(&features, &state);
    
    ASSERT_EQUAL(CMD_BLINK, cmd, "BLINK command detected");
}

/* Test command priority: BLINK > FOCUS > RELAX */
void test_command_priority() {
    TEST_START("Command Priority");
    
    classifier_state_t state;
    classifier_init(&state);
    
    features_t features;
    features.alpha_power = 0.7f;   /* Would trigger RELAX */
    features.beta_power = 0.7f;    /* Would trigger FOCUS */
    features.peak_amplitude = 500.0f;  /* Should trigger BLINK (highest priority) */
    features.variance = 10000.0f;
    
    /* BLINK should be detected first */
    classify_command(&features, &state);
    classify_command(&features, &state);
    command_t cmd = classify_command(&features, &state);
    
    ASSERT_EQUAL(CMD_BLINK, cmd, "BLINK has highest priority");
}

/* Test debouncing prevents false positives */
void test_debouncing() {
    TEST_START("Debouncing Logic");
    
    classifier_state_t state;
    classifier_init(&state);
    
    features_t features_focus;
    features_focus.alpha_power = 0.3f;
    features_focus.beta_power = 0.7f;
    features_focus.peak_amplitude = 2.0f;  /* Normal amplitude */
    features_focus.variance = 100.0f;
    
    features_t features_relax;
    features_relax.alpha_power = 0.7f;
    features_relax.beta_power = 0.3f;
    features_relax.peak_amplitude = 2.0f;  /* Normal amplitude */
    features_relax.variance = 100.0f;
    
    /* Alternate between FOCUS and RELAX - should not trigger */
    command_t cmd1 = classify_command(&features_focus, &state);
    command_t cmd2 = classify_command(&features_relax, &state);
    command_t cmd3 = classify_command(&features_focus, &state);
    
    ASSERT_EQUAL(CMD_NONE, cmd1, "Alternating signals don't trigger (1)");
    ASSERT_EQUAL(CMD_NONE, cmd2, "Alternating signals don't trigger (2)");
    ASSERT_EQUAL(CMD_NONE, cmd3, "Alternating signals don't trigger (3)");
}

/* Test baseline updates */
void test_baseline_update() {
    TEST_START("Baseline Update");
    
    classifier_state_t state;
    classifier_init(&state);
    
    float initial_baseline = state.baseline_amplitude;
    ASSERT_FLOAT_EQUAL(1.0f, initial_baseline, 0.01f, "Initial baseline is 1.0");
    
    features_t features;
    features.alpha_power = 0.7f;
    features.beta_power = 0.3f;
    features.peak_amplitude = 2.5f;  /* Realistic amplitude for baseline update */
    features.variance = 100.0f;
    
    /* Run through debouncing - triggers on 2nd call */
    classify_command(&features, &state);
    classify_command(&features, &state);
    
    /* Baseline should have updated */
    ASSERT_TRUE(state.baseline_amplitude != initial_baseline, 
                "Baseline updated after detection");
}

int main() {
    TEST_SUITE_START("Classifier Tests");
    
    /* Run tests */
    test_focus_detection();
    test_relax_detection();
    test_blink_detection();
    test_command_priority();
    test_debouncing();
    test_baseline_update();
    
    TEST_SUITE_END();
    
    return tests_failed > 0 ? 1 : 0;
}
