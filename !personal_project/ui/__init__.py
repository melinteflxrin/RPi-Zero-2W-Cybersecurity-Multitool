"""UI module - console utilities and styling."""

from .console import (
    # Colors
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
    LIGHT_BLACK, LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE, LIGHT_MAGENTA, LIGHT_CYAN, LIGHT_WHITE,
    # Styles
    RESET, BRIGHT, BOLD, DIM, UNDERLINE, BLINK, REVERSE, HIDDEN,
    # Functions
    cprint, iprint, wprint, eprint, sprint, cinput, clear, print_banner, print_line
)

__all__ = [
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
    'LIGHT_BLACK', 'LIGHT_RED', 'LIGHT_GREEN', 'LIGHT_YELLOW', 'LIGHT_BLUE', 'LIGHT_MAGENTA', 'LIGHT_CYAN', 'LIGHT_WHITE',
    'RESET', 'BRIGHT', 'BOLD', 'DIM', 'UNDERLINE', 'BLINK', 'REVERSE', 'HIDDEN',
    'cprint', 'iprint', 'wprint', 'eprint', 'sprint', 'cinput', 'clear', 'print_banner', 'print_line'
]
