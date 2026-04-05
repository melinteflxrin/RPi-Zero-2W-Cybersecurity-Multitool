"""
Terminal color codes and console utilities for styled output.

Provides ANSI color codes and helper functions for terminal output.
"""

# Regular colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Light/Bright colors
LIGHT_BLACK = '\033[90m'
LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'
LIGHT_YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_CYAN = '\033[96m'
LIGHT_WHITE = '\033[97m'

# Styles
RESET = '\033[0m'
BRIGHT = '\033[1m'
BOLD = '\033[1m'
DIM = '\033[2m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'
HIDDEN = '\033[8m'


def cprint(text, color=CYAN, end='\n'):
    """
    Print colored text.
    
    Args:
        text (str): Text to print.
        color (str): ANSI color code (default: CYAN).
        end (str): String appended after the text (default: newline).
    """
    print(f"{color}{text}{RESET}", end=end)


def iprint(text, end='\n'):
    """Print info message in light blue."""
    print(f"{LIGHT_BLUE}[INFO] {text}{RESET}", end=end)


def wprint(text, end='\n'):
    """Print warning message in yellow."""
    print(f"{YELLOW}[WARN] {text}{RESET}", end=end)


def eprint(text, end='\n'):
    """Print error message in red."""
    print(f"{RED}[ERROR] {text}{RESET}", end=end)


def sprint(text, end='\n'):
    """Print success message in green."""
    print(f"{GREEN}[✓] {text}{RESET}", end=end)


def cinput(prompt, color=LIGHT_CYAN):
    """
    Get colored input from user.
    
    Args:
        prompt (str): Input prompt text.
        color (str): ANSI color code for prompt (default: LIGHT_CYAN).
    
    Returns:
        str: User input.
    """
    return input(f"{color}{prompt}{RESET} > ")


def clear():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(text, color=CYAN):
    """Print a centered banner with borders."""
    width = 60
    print(f"\n{color}{'='*width}")
    print(f"{text:^{width}}")
    print(f"{'='*width}{RESET}\n")


def print_line(color=CYAN):
    """Print a horizontal line."""
    print(f"{color}{'-'*60}{RESET}")
