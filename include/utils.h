#ifndef UTILS_H
#define UTILS_H

#include "types.h"
#include <stdio.h>

/* Simple random number generator for noise */
float random_float(float min, float max);

/* Seed random number generator */
void seed_random(unsigned int seed);

/* Print signal buffer for debugging */
void print_signal(const signal_t *signal, size_t length, const char *label);

/* Print features for debugging */
void print_features(const features_t *features);

/* Delay function (milliseconds) */
void delay_ms(unsigned int ms);

/* Get current time in seconds (for simulation) */
float get_time_sec(void);

/* Console color codes for output */
#define COLOR_RESET   "\033[0m"
#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_BLUE    "\033[34m"
#define COLOR_MAGENTA "\033[35m"
#define COLOR_CYAN    "\033[36m"
#define COLOR_WHITE   "\033[37m"

#endif /* UTILS_H */
