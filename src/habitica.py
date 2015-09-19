""" Module "Habitica" : Main Driver Program

    The main program is launched from this module
"""
# Standard Library Imports
import curses
import tempfile
import time

# Custom Module Imports

# from import * is bad practice, but we use it just for convenience in case of
# constants
from config import *
from screen import Screen

user_id = ''
api_token = ''


def main(curses_screen):
    screen = Screen(curses_screen)
    screen.Initialize()

    screen.Display("Just testing...")
    screen.DisplayBold("Bold", 1)
    screen.DisplayCustomColor("Red", SCR_COLOR_RED, 2)
    screen.DisplayCustomColor("Green", SCR_COLOR_GREEN, 3)
    screen.DisplayCustomColor("Blue", SCR_COLOR_BLUE, 4)
    screen.DisplayCustomColor("Yellow", SCR_COLOR_YELLOW, 5)
    screen.DisplayCustomColor("White", SCR_COLOR_WHITE, 6)
    screen.DisplayCustomColor("LightOrange", SCR_COLOR_LIGHT_ORANGE, 7)
    screen.DisplayCustomColor("DarkOrange", SCR_COLOR_DARK_ORANGE, 8)
    screen.Clear()
    time.sleep(3)
    screen.Display("Exiting...")
    time.sleep(1)


curses.wrapper(main)
