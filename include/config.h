#ifndef CONFIG_H
#define CONFIG_H

/* ========== Signal Generation Parameters ========== */
#define SAMPLING_RATE       256     /* Hz - typical for EEG */
#define WINDOW_SIZE         256     /* samples (1 second of data) */
#define SIGNAL_DURATION     10      /* seconds for demo */

/* ========== Frequency Bands ========== */
#define ALPHA_LOW_FREQ      8.0f    /* Hz */
#define ALPHA_HIGH_FREQ     13.0f   /* Hz */
#define BETA_LOW_FREQ       13.0f   /* Hz */
#define BETA_HIGH_FREQ      30.0f   /* Hz */

/* ========== Signal Amplitudes ========== */
#define ALPHA_AMPLITUDE     50.0f   /* microvolts */
#define BETA_AMPLITUDE      30.0f   /* microvolts */
#define BLINK_AMPLITUDE     200.0f  /* microvolts */
#define NOISE_LEVEL         5.0f    /* microvolts */

/* ========== Classification Thresholds ========== */
#define FOCUS_THRESHOLD     0.6f    /* Beta power ratio */
#define RELAX_THRESHOLD     0.6f    /* Alpha power ratio */
#define BLINK_THRESHOLD     3.0f    /* Amplitude multiplier above baseline */
#define DEBOUNCE_COUNT      3       /* Consecutive samples needed */

/* ========== Filter Parameters ========== */
#define MA_FILTER_SIZE      5       /* Moving average window */
#define BASELINE_SAMPLES    50      /* Samples for baseline calculation */

/* ========== Output Control ========== */
#define CURSOR_MAX_X        10
#define CURSOR_MAX_Y        10
#define BUZZER_DURATION_MS  200

/* ========== Debug Options ========== */
#define DEBUG_SIGNALS       1       /* Print signal values */
#define DEBUG_FEATURES      1       /* Print extracted features */
#define DEBUG_COMMANDS      1       /* Print detected commands */

/* ========== Mathematical Constants ========== */
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#endif /* CONFIG_H */
