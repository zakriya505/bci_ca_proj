#ifndef DATA_LOADER_H
#define DATA_LOADER_H

#include "types.h"
#include "config.h"
#include <stdio.h>

/* Maximum path length */
#define MAX_PATH_LENGTH 512

/* Data configuration structure */
typedef struct {
    char data_directory[MAX_PATH_LENGTH];
    char default_dataset[MAX_PATH_LENGTH];
    bool_t auto_detect_format;
} data_config_t;

/* Dataset metadata */
typedef struct {
    char filename[MAX_PATH_LENGTH];
    size_t num_samples;
    size_t num_channels;
    float sampling_rate;
    bool_t has_labels;
} dataset_info_t;

/* Sample with metadata from CSV */
typedef struct {
    float time;
    signal_t amplitude;
    float alpha_power;
    float beta_power;
    command_t command;
} eeg_sample_t;

/* Initialize data loader with configuration */
void data_loader_init(const data_config_t *config);

/* Load dataset from CSV file */
bool_t load_dataset_csv(const char *filepath, eeg_sample_t *samples, 
                        size_t max_samples, size_t *num_loaded);

/* Get dataset information without loading full data */
bool_t get_dataset_info(const char *filepath, dataset_info_t *info);

/* Set data directory path */
void set_data_directory(const char *path);

/* Get full path to dataset file */
bool_t get_dataset_path(const char *dataset_name, char *output_path);

/* Parse command string to command_t enum */
command_t parse_command_string(const char *cmd_str);

/* Cleanup data loader resources */
void data_loader_cleanup(void);

#endif /* DATA_LOADER_H */
