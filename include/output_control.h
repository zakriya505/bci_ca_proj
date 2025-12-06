#ifndef OUTPUT_CONTROL_H
#define OUTPUT_CONTROL_H

#include "types.h"
#include "config.h"

/* Initialize output control system */
void output_control_init(output_state_t *state);

/* Execute command on output devices */
void execute_command(command_t cmd, output_state_t *state);

/* Display current output state */
void display_output_state(const output_state_t *state);

/* Control virtual LED */
void set_led(output_state_t *state, bool_t on);

/* Trigger virtual buzzer */
void trigger_buzzer(output_state_t *state);

/* Move cursor */
void move_cursor(output_state_t *state, int dx, int dy);

/* Select character at cursor position */
void select_character(output_state_t *state);

/* Display visual LED representation */
void display_led(bool_t state);

/* Display buzzer activation */
void display_buzzer(void);

#endif /* OUTPUT_CONTROL_H */
