#include "data_loader.h"
#include "utils.h"
#include <string.h>
#include <stdlib.h>

/* Global data configuration */
static data_config_t g_data_config;
static bool_t g_initialized = FALSE;

void data_loader_init(const data_config_t *config) {
    if (config != NULL) {
        memcpy(&g_data_config, config, sizeof(data_config_t));
    } else {
        /* Default configuration */
        strcpy(g_data_config.data_directory, "data/raw");
        strcpy(g_data_config.default_dataset, "sample_eeg_data.csv");
        g_data_config.auto_detect_format = TRUE;
    }
    g_initialized = TRUE;
}

void set_data_directory(const char *path) {
    if (path != NULL && strlen(path) < MAX_PATH_LENGTH) {
        strcpy(g_data_config.data_directory, path);
    }
}

bool_t get_dataset_path(const char *dataset_name, char *output_path) {
    if (!g_initialized) {
        data_loader_init(NULL);
    }
    
    if (dataset_name == NULL || output_path == NULL) {
        return FALSE;
    }
    
    /* Check if dataset_name already has path */
    if (strchr(dataset_name, '/') != NULL || strchr(dataset_name, '\\') != NULL) {
        strcpy(output_path, dataset_name);
        return TRUE;
    }
    
    /* Construct path: data_directory/dataset_name */
    snprintf(output_path, MAX_PATH_LENGTH, "%s/%s", 
             g_data_config.data_directory, dataset_name);
    
    return TRUE;
}

command_t parse_command_string(const char *cmd_str) {
    if (cmd_str == NULL) {
        return CMD_NONE;
    }
    
    if (strcmp(cmd_str, "FOCUS") == 0) {
        return CMD_FOCUS;
    } else if (strcmp(cmd_str, "RELAX") == 0) {
        return CMD_RELAX;
    } else if (strcmp(cmd_str, "BLINK") == 0) {
        return CMD_BLINK;
    } else {
        return CMD_NONE;
    }
}

bool_t get_dataset_info(const char *filepath, dataset_info_t *info) {
    if (filepath == NULL || info == NULL) {
        return FALSE;
    }
    
    FILE *fp = fopen(filepath, "r");
    if (fp == NULL) {
        return FALSE;
    }
    
    /* Initialize info */
    strcpy(info->filename, filepath);
    info->num_samples = 0;
    info->num_channels = 1; /* Default single channel */
    info->sampling_rate = SAMPLING_RATE;
    info->has_labels = FALSE;
    
    char line[512];
    
    /* Read header line */
    if (fgets(line, sizeof(line), fp) != NULL) {
        /* Check if has command column */
        if (strstr(line, "command") != NULL) {
            info->has_labels = TRUE;
        }
    }
    
    /* Count samples */
    while (fgets(line, sizeof(line), fp) != NULL) {
        info->num_samples++;
    }
    
    fclose(fp);
    return TRUE;
}

bool_t load_dataset_csv(const char *filepath, eeg_sample_t *samples, 
                        size_t max_samples, size_t *num_loaded) {
    if (filepath == NULL || samples == NULL || num_loaded == NULL) {
        return FALSE;
    }
    
    FILE *fp = fopen(filepath, "r");
    if (fp == NULL) {
        log_error("Failed to open dataset file: %s", filepath);
        return FALSE;
    }
    
    char line[512];
    size_t sample_count = 0;
    
    /* Skip header line */
    if (fgets(line, sizeof(line), fp) == NULL) {
        fclose(fp);
        return FALSE;
    }
    
    /* Read data lines */
    while (fgets(line, sizeof(line), fp) != NULL && sample_count < max_samples) {
        eeg_sample_t *sample = &samples[sample_count];
        char cmd_str[32];
        
        /* Parse CSV line: time,amplitude,alpha_power,beta_power,command */
        int fields = sscanf(line, "%f,%f,%f,%f,%31s",
                           &sample->time,
                           &sample->amplitude,
                           &sample->alpha_power,
                           &sample->beta_power,
                           cmd_str);
        
        if (fields >= 4) {
            /* Parse command if present */
            if (fields == 5) {
                sample->command = parse_command_string(cmd_str);
            } else {
                sample->command = CMD_NONE;
            }
            
            sample_count++;
        }
    }
    
    fclose(fp);
    *num_loaded = sample_count;
    
    log_info("Loaded %zu samples from %s", sample_count, filepath);
    
    return sample_count > 0;
}

void data_loader_cleanup(void) {
    g_initialized = FALSE;
}
