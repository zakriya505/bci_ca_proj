#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>
#include <stddef.h>

/* Boolean type */
typedef enum {
    FALSE = 0,
    TRUE = 1
} bool_t;

/* EEG signal sample type */
typedef float signal_t;

/* Command types that can be detected */
typedef enum {
    CMD_NONE = 0,
    CMD_FOCUS,      /* High beta activity - turn LED ON */
    CMD_RELAX,      /* High alpha activity - turn LED OFF */
    CMD_BLINK       /* Sharp spike - trigger action */
} command_t;

/* Mental state representation */
typedef struct {
    signal_t alpha_power;    /* Power in alpha band (8-13 Hz) */
    signal_t beta_power;     /* Power in beta band (13-30 Hz) */
    signal_t peak_amplitude; /* Maximum amplitude for blink detection */
    signal_t variance;       /* Signal variance */
} features_t;

/* Output device states */
typedef struct {
    bool_t led_state;        /* LED ON/OFF */
    bool_t buzzer_active;    /* Buzzer active/inactive */
    int cursor_x;            /* Cursor X position */
    int cursor_y;            /* Cursor Y position */
    char selected_char;      /* Currently selected character */
} output_state_t;

#endif /* TYPES_H */
