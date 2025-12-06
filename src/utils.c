#include "utils.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>

static unsigned int random_seed = 0;
static clock_t start_time = 0;

void seed_random(unsigned int seed) {
    random_seed = seed;
    srand(seed);
}

float random_float(float min, float max) {
    float scale = rand() / (float)RAND_MAX;
    return min + scale * (max - min);
}

void print_signal(const signal_t *signal, size_t length, const char *label) {
    printf("\n%s[SIGNAL: %s]%s\n", COLOR_CYAN, label, COLOR_RESET);
    printf("Length: %zu samples\n", length);
    
    if (length <= 10) {
        for (size_t i = 0; i < length; i++) {
            printf("  [%zu] %.2f\n", i, signal[i]);
        }
    } else {
        printf("  First 5: ");
        for (size_t i = 0; i < 5; i++) {
            printf("%.2f ", signal[i]);
        }
        printf("\n  Last 5:  ");
        for (size_t i = length - 5; i < length; i++) {
            printf("%.2f ", signal[i]);
        }
        printf("\n");
    }
}

void print_features(const features_t *features) {
    printf("\n%s[FEATURES]%s\n", COLOR_YELLOW, COLOR_RESET);
    printf("  Alpha Power:     %.4f\n", features->alpha_power);
    printf("  Beta Power:      %.4f\n", features->beta_power);
    printf("  Peak Amplitude:  %.4f\n", features->peak_amplitude);
    printf("  Variance:        %.4f\n", features->variance);
}

void delay_ms(unsigned int ms) {
    clock_t start = clock();
    while ((clock() - start) * 1000 / CLOCKS_PER_SEC < ms);
}

float get_time_sec(void) {
    if (start_time == 0) {
        start_time = clock();
    }
    return (float)(clock() - start_time) / CLOCKS_PER_SEC;
}
