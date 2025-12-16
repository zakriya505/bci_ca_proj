#ifndef CONFIG_H
#define CONFIG_H

/* ========== Signal Generation Parameters ========== */
#define SAMPLING_RATE       256     /* Hz - typical for EEG */
#define WINDOW_SIZE         256     /* samples (1 second of data) */
#define SIGNAL_DURATION     10      /* seconds for demo */

/* ========== Frequency Bands ========== */
#define THETA_LOW_FREQ      4.0f    /* Hz - attention, drowsiness */
#define THETA_HIGH_FREQ     8.0f    /* Hz */
#define ALPHA_LOW_FREQ      8.0f    /* Hz - relaxation, visual processing */
#define ALPHA_HIGH_FREQ     13.0f   /* Hz */
#define BETA_LOW_FREQ       13.0f   /* Hz - focus, motor control */
#define BETA_HIGH_FREQ      30.0f   /* Hz */
#define GAMMA_LOW_FREQ      30.0f   /* Hz - cognitive function */
#define GAMMA_HIGH_FREQ     50.0f   /* Hz */

/* ========== FFT Configuration ========== */
/* Enable FFT-based band power calculation (more accurate) */
#define USE_FFT_BANDPOWER    1      /* Set to 0 for faster approximate method */

/* ========== Signal Amplitudes ========== */
#define ALPHA_AMPLITUDE     50.0f   /* microvolts */
#define BETA_AMPLITUDE      30.0f   /* microvolts */
#define BLINK_AMPLITUDE     200.0f  /* microvolts */
#define NOISE_LEVEL         5.0f    /* microvolts */

/* ========== Classification Thresholds ========== */
#define FOCUS_THRESHOLD     0.6f    /* Beta power ratio */
#define RELAX_THRESHOLD     0.6f    /* Alpha power ratio */
#define BLINK_THRESHOLD     3.0f    /* Amplitude multiplier above baseline */
#define DEBOUNCE_COUNT      2       /* Consecutive samples needed (reduced for faster response) */

/* ========== Health Prediction Thresholds ========== */
/* Visual Impairment: Low alpha during relaxed states (occipital lobe) */
#define VISUAL_ALPHA_NORMAL      0.35f   /* Normal alpha power threshold */
#define VISUAL_ALPHA_BORDERLINE  0.25f   /* Borderline threshold */

/* Motor Impairment: Abnormal beta/mu rhythm (motor cortex) */
#define MOTOR_BETA_NORMAL        0.30f   /* Normal beta power threshold */
#define MOTOR_BETA_BORDERLINE    0.20f   /* Borderline threshold */

/* Attention Deficit: High theta/beta ratio (frontal lobe) */
#define ATTENTION_RATIO_NORMAL   1.5f    /* Normal theta/beta ratio */
#define ATTENTION_RATIO_BORDER   2.0f    /* Borderline ratio */


/* ========== Filter Parameters ========== */
#define MA_FILTER_SIZE      5       /* Moving average window */
#define BASELINE_SAMPLES    50      /* Samples for baseline calculation */

/* ========== Output Control ========== */
#define CURSOR_MAX_X        10
#define CURSOR_MAX_Y        10
#define BUZZER_DURATION_MS  200

/* ========== Debug Options ========== */
#define DEBUG_SIGNALS       0       /* Print signal values */
#define DEBUG_FEATURES      0       /* Print extracted features */
#define DEBUG_COMMANDS      0       /* Print detected commands */

/* ========== Mathematical Constants ========== */
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#endif /* CONFIG_H */
