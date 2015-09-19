""" Module "Config" : Global Config File

    This file contains all the constants used in the program that pertain
    to the configuration of the terminal
"""

import curses

NUM_CONTEXT_REGISTERS = 4

# Colors
SCR_COLOR_RED          = 2
SCR_COLOR_GREEN        = 3
SCR_COLOR_YELLOW       = 4
SCR_COLOR_BLUE         = 5
SCR_COLOR_WHITE        = 6
SCR_COLOR_MAGENTA      = 7
SCR_COLOR_LIGHT_ORANGE = 8
SCR_COLOR_DARK_ORANGE  = 9

# Display Colors with Background
SCR_COLOR_BLUE_GRAY_BGRD = 10
SCR_COLOR_GRAY_BLUE_BGRD = 11

# Background Color (Default black)
SCR_COLOR_BGRD = curses.COLOR_BLACK
