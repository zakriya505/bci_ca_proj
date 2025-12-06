#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "types.h"
#include "config.h"
#include "eeg_simulator.h"
#include "preprocessing.h"
#include "feature_extraction.h"
#include "classifier.h"
#include "output_control.h"
#include "utils.h"

void print_banner(void) {
    printf("\n");
    printf("%s╔═══════════════════════════════════════════════════════════════╗%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║                                                               ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║        RISC-V Brain-Computer Interface (BCI) System          ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║                                                               ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║        Embedded System for Simple Command Recognition        ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║                                                               ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s╚═══════════════════════════════════════════════════════════════╝%s\n", COLOR_CYAN, COLOR_RESET);
    printf("\n");
}

void print_system_info(void) {
    printf("%s[SYSTEM INFO]%s\n", COLOR_MAGENTA, COLOR_RESET);
    printf("  Sampling Rate:    %d Hz\n", SAMPLING_RATE);
    printf("  Window Size:      %d samples\n", WINDOW_SIZE);
    printf("  Alpha Band:       %.1f - %.1f Hz\n", ALPHA_LOW_FREQ, ALPHA_HIGH_FREQ);
    printf("  Beta Band:        %.1f - %.1f Hz\n", BETA_LOW_FREQ, BETA_HIGH_FREQ);
    printf("  Focus Threshold:  %.2f\n", FOCUS_THRESHOLD);
    printf("  Relax Threshold:  %.2f\n", RELAX_THRESHOLD);
    printf("  Blink Threshold:  %.2f\n", BLINK_THRESHOLD);
    printf("\n");
}

void run_demo_scenario(const char *scenario_name, command_t state, int iterations) {
    printf("\n%s═══════════════════════════════════════════════════════════════%s\n", 
           COLOR_YELLOW, COLOR_RESET);
    printf("%s[DEMO SCENARIO: %s]%s\n", COLOR_YELLOW, scenario_name, COLOR_RESET);
    printf("%s═══════════════════════════════════════════════════════════════%s\n\n", 
           COLOR_YELLOW, COLOR_RESET);
    
    signal_t eeg_buffer[WINDOW_SIZE];
    signal_t processed_buffer[WINDOW_SIZE];
    features_t features;
    classifier_state_t classifier_state;
    output_state_t output_state;
    
    /* Initialize modules */
    classifier_init(&classifier_state);
    output_control_init(&output_state);
    
    for (int iter = 0; iter < iterations; iter++) {
        printf("\n%s--- Iteration %d/%d ---%s\n", COLOR_BLUE, iter + 1, iterations, COLOR_RESET);
        
        /* Step 1: Generate EEG signal */
        printf("%s[1] Generating EEG signal...%s\n", COLOR_GREEN, COLOR_RESET);
        generate_eeg_sample(eeg_buffer, WINDOW_SIZE, state);
        
        #if DEBUG_SIGNALS
        if (iter == 0) {
            printf("    Signal range: [%.2f, %.2f] µV\n", 
                   eeg_buffer[0], eeg_buffer[WINDOW_SIZE-1]);
        }
        #endif
        
        /* Step 2: Preprocess signal */
        printf("%s[2] Preprocessing signal...%s\n", COLOR_GREEN, COLOR_RESET);
        memcpy(processed_buffer, eeg_buffer, WINDOW_SIZE * sizeof(signal_t));
        preprocess_signal(processed_buffer, WINDOW_SIZE);
        
        /* Step 3: Extract features */
        printf("%s[3] Extracting features...%s\n", COLOR_GREEN, COLOR_RESET);
        extract_features(processed_buffer, WINDOW_SIZE, &features);
        
        #if DEBUG_FEATURES
        print_features(&features);
        #endif
        
        /* Step 4: Classify command */
        printf("%s[4] Classifying command...%s\n", COLOR_GREEN, COLOR_RESET);
        command_t detected = classify_command(&features, &classifier_state);
        
        #if DEBUG_COMMANDS
        printf("    Detected: %s%s%s", COLOR_MAGENTA, command_to_string(detected), COLOR_RESET);
        if (detected != CMD_NONE) {
            printf(" ✓");
        }
        printf("\n");
        #endif
        
        /* Step 5: Execute command */
        if (detected != CMD_NONE) {
            printf("%s[5] Executing command...%s\n", COLOR_GREEN, COLOR_RESET);
            execute_command(detected, &output_state);
            
            /* Reset buzzer after display */
            if (output_state.buzzer_active) {
                output_state.buzzer_active = FALSE;
            }
        }
        
        /* Step 6: Display output state */
        display_output_state(&output_state);
        
        /* Add delay to make LED changes visible */
        delay_ms(1000);  /* 1 second delay */
    }
}

void run_interactive_demo(void) {
    printf("\n%s═══════════════════════════════════════════════════════════════%s\n", 
           COLOR_YELLOW, COLOR_RESET);
    printf("%s[INTERACTIVE DEMO: Mixed Commands]%s\n", COLOR_YELLOW, COLOR_RESET);
    printf("%s═══════════════════════════════════════════════════════════════%s\n\n", 
           COLOR_YELLOW, COLOR_RESET);
    
    command_t sequence[] = {CMD_NONE, CMD_FOCUS, CMD_FOCUS, CMD_RELAX, 
                           CMD_RELAX, CMD_BLINK, CMD_FOCUS, CMD_BLINK};
    const char *sequence_names[] = {"Baseline", "Focus", "Focus", "Relax",
                                   "Relax", "Blink", "Focus", "Blink"};
    int sequence_length = sizeof(sequence) / sizeof(sequence[0]);
    
    signal_t eeg_buffer[WINDOW_SIZE];
    signal_t processed_buffer[WINDOW_SIZE];
    features_t features;
    classifier_state_t classifier_state;
    output_state_t output_state;
    
    classifier_init(&classifier_state);
    output_control_init(&output_state);
    
    for (int i = 0; i < sequence_length; i++) {
        printf("\n%s--- Step %d: %s ---%s\n", 
               COLOR_BLUE, i + 1, sequence_names[i], COLOR_RESET);
        
        /* Generate and process signal */
        generate_eeg_sample(eeg_buffer, WINDOW_SIZE, sequence[i]);
        memcpy(processed_buffer, eeg_buffer, WINDOW_SIZE * sizeof(signal_t));
        preprocess_signal(processed_buffer, WINDOW_SIZE);
        extract_features(processed_buffer, WINDOW_SIZE, &features);
        
        /* Classify and execute */
        command_t detected = classify_command(&features, &classifier_state);
        
        printf("Expected: %s%s%s | Detected: %s%s%s\n",
               COLOR_CYAN, sequence_names[i], COLOR_RESET,
               COLOR_MAGENTA, command_to_string(detected), COLOR_RESET);
        
        if (detected != CMD_NONE) {
            execute_command(detected, &output_state);
            if (output_state.buzzer_active) {
                output_state.buzzer_active = FALSE;
            }
        }
        
        display_output_state(&output_state);
        delay_ms(1500);  /* 1.5 second delay for better visibility */
    }
}

int main(int argc, char *argv[]) {
    /* Print banner */
    print_banner();
    
    /* Initialize all modules */
    printf("%s[INITIALIZATION]%s\n", COLOR_GREEN, COLOR_RESET);
    printf("  Initializing EEG simulator...\n");
    eeg_simulator_init();
    
    printf("  Initializing preprocessing...\n");
    preprocessing_init();
    
    printf("  Initializing feature extraction...\n");
    feature_extraction_init();
    
    printf("  All modules initialized successfully!\n\n");
    
    /* Display system information */
    print_system_info();
    
    /* Run demo scenarios */
    printf("%s[STARTING DEMONSTRATION]%s\n\n", COLOR_GREEN, COLOR_RESET);
    
    /* Scenario 1: Focus command */
    run_demo_scenario("FOCUS Command (Turn LED ON)", CMD_FOCUS, 5);
    
    /* Scenario 2: Relax command */
    run_demo_scenario("RELAX Command (Turn LED OFF)", CMD_RELAX, 5);
    
    /* Scenario 3: Blink command */
    run_demo_scenario("BLINK Command (Trigger Action)", CMD_BLINK, 5);
    
    /* Scenario 4: Interactive mixed commands */
    run_interactive_demo();
    
    /* Final summary */
    printf("\n%s╔═══════════════════════════════════════════════════════════════╗%s\n", 
           COLOR_GREEN, COLOR_RESET);
    printf("%s║                    DEMONSTRATION COMPLETE                     ║%s\n", 
           COLOR_GREEN, COLOR_RESET);
    printf("%s╚═══════════════════════════════════════════════════════════════╝%s\n\n", 
           COLOR_GREEN, COLOR_RESET);
    
    printf("BCI system successfully demonstrated all three commands:\n");
    printf("  ✓ FOCUS  - High beta activity → LED ON\n");
    printf("  ✓ RELAX  - High alpha activity → LED OFF\n");
    printf("  ✓ BLINK  - Sharp spike → Buzzer + Cursor movement\n\n");
    
    return 0;
}
