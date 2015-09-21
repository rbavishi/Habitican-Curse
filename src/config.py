""" Module "Config" : Global Config File

    This file contains all the constants used in the program that pertain
    to the configuration of the terminal
"""

import curses

NUM_CONTEXT_REGISTERS = 4

# Screen Specifications - Will be adjusted during runtime
SCR_MAX_MENU_ROWS   = 10
SCR_X = 0
SCR_Y = 0
SCR_MENU_ITEM_WIDTH = 0

# Colors
SCR_COLOR_RED          = 2
SCR_COLOR_GREEN        = 3
SCR_COLOR_YELLOW       = 4
SCR_COLOR_BLUE         = 5
SCR_COLOR_WHITE        = 6
SCR_COLOR_MAGENTA      = 7
SCR_COLOR_CYAN         = 14
SCR_COLOR_LIGHT_ORANGE = 8
SCR_COLOR_DARK_ORANGE  = 9
SCR_COLOR_DARK_GRAY    = 15
SCR_COLOR_LIGHT_GRAY    = 16

# Display Colors with Background
SCR_COLOR_BLUE_GRAY_BGRD = 10
SCR_COLOR_GRAY_BLUE_BGRD = 11
SCR_COLOR_WHITE_GRAY_BGRD = 12
SCR_COLOR_GRAY_WHITE_BGRD = 13

# Background Color (Default black)
SCR_COLOR_BGRD = curses.COLOR_BLACK

# Special Symbols
SYMBOL_TICK = u'\u2714'.encode("utf-8")
SYMBOL_DISC = u'\u25CF'.encode("utf-8")
SYMBOL_DOWN_TRIANGLE = u'\u25BC'.encode("utf-8")
SYMBOL_UP_TRIANGLE = u'\u25B2'.encode("utf-8")
SYMBOL_DELETE = 'x'
SYMBOL_HEART = u'\u2665'.encode("utf-8")
SYMBOL_EXPERIENCE = u'\u2605'.encode("utf-8")
SYMBOL_GOLD = u'\u25CF'.encode("utf-8")
SYMBOL_MANA = u'\u2600'.encode("utf-8")
SYMBOL_EDIT = u'\u270E'.encode("utf-8")

# Status Attributes
HabitStatus = {'+': False, '-': False, SYMBOL_DELETE: False, SYMBOL_EDIT: False}
HabitPosStatus = {'+': False, SYMBOL_DELETE: False, SYMBOL_EDIT: False}
HabitNegStatus = {'-': False, SYMBOL_DELETE: False, SYMBOL_EDIT: False}
TODODailyStatus = {SYMBOL_TICK: False, SYMBOL_DELETE: False, SYMBOL_EDIT: False}
ChecklistStatus = {SYMBOL_TICK: False, SYMBOL_DELETE: False, SYMBOL_EDIT: False}

# Function for setting values at runtime

def ConfigureRuntime(screen):
    global SCR_Y, SCR_X, SCR_MENU_ITEM_WIDTH
    SCR_X, SCR_Y = screen.getmaxyx()
    SCR_MENU_ITEM_WIDTH = (SCR_Y - 10)/3


