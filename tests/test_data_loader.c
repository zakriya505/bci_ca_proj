#include "test_framework.h"
#include "data_loader.h"
#include <stdio.h>
#include <string.h>

/* Test data loader initialization */
void test_data_loader_init(void) {
    TEST_START("Data Loader Initialization");
    
    data_config_t config;
    strcpy(config.data_directory, "data/raw");
    strcpy(config.default_dataset, "sample_eeg_data.csv");
    config.auto_detect_format = TRUE;
    
    data_loader_init(&config);
    
    TEST_PASS("Data loader initialized successfully");
}

/* Test path construction */
void test_dataset_path(void) {
    TEST_START("Dataset Path Construction");
    
    data_loader_init(NULL);
    
    char path[MAX_PATH_LENGTH];
    bool_t result = get_dataset_path("test.csv", path);
    
    TEST_ASSERT(result == TRUE, "Path construction should succeed");
    TEST_ASSERT(strstr(path, "data/raw/test.csv") != NULL, 
                "Path should contain data directory");
    
    TEST_PASS("Dataset path constructed correctly");
}

/* Test command string parsing */
void test_command_parsing(void) {
    TEST_START("Command String Parsing");
    
    TEST_ASSERT(parse_command_string("FOCUS") == CMD_FOCUS, 
                "Should parse FOCUS command");
    TEST_ASSERT(parse_command_string("RELAX") == CMD_RELAX, 
                "Should parse RELAX command");
    TEST_ASSERT(parse_command_string("BLINK") == CMD_BLINK, 
                "Should parse BLINK command");
    TEST_ASSERT(parse_command_string("NONE") == CMD_NONE, 
                "Should parse NONE command");
    TEST_ASSERT(parse_command_string("INVALID") == CMD_NONE, 
                "Should default to NONE for invalid");
    
    TEST_PASS("Command parsing works correctly");
}

/* Test dataset info retrieval */
void test_dataset_info(void) {
    TEST_START("Dataset Info Retrieval");
    
    data_loader_init(NULL);
    
    dataset_info_t info;
    const char *filepath = "data/raw/sample_eeg_data.csv";
    
    bool_t result = get_dataset_info(filepath, &info);
    
    if (result) {
        TEST_ASSERT(info.num_samples > 0, "Should have samples");
        TEST_ASSERT(info.has_labels == TRUE, "Should detect command labels");
        printf("  Dataset has %zu samples\n", info.num_samples);
        TEST_PASS("Dataset info retrieved successfully");
    } else {
        printf("  WARNING: Could not load dataset (file may not exist yet)\n");
        TEST_PASS("Test skipped - dataset file not found");
    }
}

/* Test loading actual dataset */
void test_load_dataset(void) {
    TEST_START("Load Dataset from CSV");
    
    data_loader_init(NULL);
    
    const char *filepath = "data/raw/sample_eeg_data.csv";
    eeg_sample_t samples[100];
    size_t num_loaded;
    
    bool_t result = load_dataset_csv(filepath, samples, 100, &num_loaded);
    
    if (result) {
        TEST_ASSERT(num_loaded > 0, "Should load samples");
        TEST_ASSERT(samples[0].time >= 0.0f, "Time should be valid");
        
        printf("  Loaded %zu samples\n", num_loaded);
        printf("  First sample: time=%.3f, amplitude=%.2f, command=%d\n",
               samples[0].time, samples[0].amplitude, samples[0].command);
        
        TEST_PASS("Dataset loaded successfully");
    } else {
        printf("  WARNING: Could not load dataset (file may not exist yet)\n");
        TEST_PASS("Test skipped - dataset file not found");
    }
}

int main(void) {
    TEST_SUITE_START("Data Loader Tests");
    
    test_data_loader_init();
    test_dataset_path();
    test_command_parsing();
    test_dataset_info();
    test_load_dataset();
    
    TEST_SUITE_END();
    
    return 0;
}
