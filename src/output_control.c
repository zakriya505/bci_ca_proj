#include "output_control.h"
#include "utils.h"
#include <stdio.h>

static const char keyboard_grid[10][10] = {
    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'},
    {'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'},
    {'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4'},
    {'5', '6', '7', '8', '9', '0', ' ', '.', ',', '!'},
    {'?', '-', '_', '(', ')', '[', ']', '{', '}', '/'},
    {'@', '#', '$', '%', '&', '*', '+', '=', '<', '>'},
    {'^', '~', '`', '\'', '"', ':', ';', '\\', '|', '\n'},
    {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'},
    {'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'},
    {'u', 'v', 'w', 'x', 'y', 'z', ' ', ' ', ' ', ' '}
};

void output_control_init(output_state_t *state) {
    state->led_state = FALSE;
    state->buzzer_active = FALSE;
    state->cursor_x = 0;
    state->cursor_y = 0;
    state->selected_char = 'A';
}

void set_led(output_state_t *state, bool_t on) {
    state->led_state = on;
}

void trigger_buzzer(output_state_t *state) {
    state->buzzer_active = TRUE;
}

void move_cursor(output_state_t *state, int dx, int dy) {
    state->cursor_x += dx;
    state->cursor_y += dy;
    
    /* Wrap around boundaries */
    if (state->cursor_x < 0) state->cursor_x = CURSOR_MAX_X - 1;
    if (state->cursor_x >= CURSOR_MAX_X) state->cursor_x = 0;
    if (state->cursor_y < 0) state->cursor_y = CURSOR_MAX_Y - 1;
    if (state->cursor_y >= CURSOR_MAX_Y) state->cursor_y = 0;
}

void select_character(output_state_t *state) {
    state->selected_char = keyboard_grid[state->cursor_y][state->cursor_x];
}

void display_led(bool_t state) {
    if (state) {
        printf("%s[LED] ████████ ON %s", COLOR_GREEN, COLOR_RESET);
    } else {
        printf("%s[LED] ░░░░░░░░ OFF%s", COLOR_RED, COLOR_RESET);
    }
}

void display_buzzer(void) {
    printf(" %s[BUZZER] ♪ BEEP! ♪%s", COLOR_YELLOW, COLOR_RESET);
}

void execute_command(command_t cmd, output_state_t *state) {
    switch (cmd) {
        case CMD_FOCUS:
            set_led(state, TRUE);
            break;
            
        case CMD_RELAX:
            set_led(state, FALSE);
            break;
            
        case CMD_BLINK:
            trigger_buzzer(state);
            move_cursor(state, 1, 0);
            select_character(state);
            break;
            
        case CMD_NONE:
        default:
            /* No action */
            break;
    }
}

void display_output_state(const output_state_t *state) {
    printf("\n%s╔════════════════════════════════════════════╗%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s║          OUTPUT DEVICE STATUS              ║%s\n", COLOR_CYAN, COLOR_RESET);
    printf("%s╠════════════════════════════════════════════╣%s\n", COLOR_CYAN, COLOR_RESET);
    
    printf("%s║%s ", COLOR_CYAN, COLOR_RESET);
    display_led(state->led_state);
    
    if (state->buzzer_active) {
        display_buzzer();
    }
    printf("\n");
    
    printf("%s║%s Cursor Position: (%d, %d)                  \n", 
           COLOR_CYAN, COLOR_RESET, state->cursor_x, state->cursor_y);
    printf("%s║%s Selected Character: '%c'                    \n",
           COLOR_CYAN, COLOR_RESET, state->selected_char);
    
    printf("%s╚════════════════════════════════════════════╝%s\n", COLOR_CYAN, COLOR_RESET);
}
