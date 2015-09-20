""" Module "Habitica" : Main Driver Program

    The main program is launched from this module
"""
# Standard Library Imports
import curses
import tempfile
import time
import locale
import thread

# Custom Module Imports

# from import * is bad practice, but we use it just for convenience in case of
# constants
from config import *
from screen import Screen
import global_objects as G
import helper as H
import menu as M

user_id = ''
api_token = ''

# Ability to display symbols
locale.setlocale(locale.LC_ALL, '') 


def BookKeepingThread():
    while(G.screen == None):
        i = 2
    i = 2
    while(1):
        G.screen.Display(str(i))
        i += 1
        time.sleep(2)



def main(curses_screen):
    G.screen = Screen(curses_screen)
    G.screen.Initialize()


    G.screen.Display("Just testing...")
    G.screen.DisplayBold("Bold", 1)
    G.screen.DisplayBold(SYMBOL_HEART, 9)
    G.screen.DisplayBold(SYMBOL_DISC, 10)
    G.screen.DisplayBold(SYMBOL_EDIT, 11)
    G.screen.DisplayCustomColor(str(G.screen.SCR_MENU_ITEM_WIDTH), SCR_COLOR_RED, 2)
    G.screen.DisplayCustomColor("Cyan", SCR_COLOR_CYAN, 12)
    G.screen.DisplayCustomColor("Green", SCR_COLOR_GREEN, 3)
    G.screen.DisplayCustomColor("Blue", SCR_COLOR_BLUE, 4)
    G.screen.DisplayCustomColor("Yellow", SCR_COLOR_YELLOW, 5)
    G.screen.DisplayCustomColor("White", SCR_COLOR_WHITE, 6)
    G.screen.DisplayCustomColor("LightOrange", SCR_COLOR_LIGHT_ORANGE, 7)
    G.screen.DisplayCustomColor("DarkOrange", SCR_COLOR_DARK_ORANGE, 8)

    status = H.Status({'+': True, '-': False,  SYMBOL_TICK: False}, [0, 1],
    '[24/10]')
    status.SetXY(20, 20)
    status.Display()
    menu_item = [M.MenuItem('a'), M.MenuItem('b'), M.MenuItem('c')]
    menu = M.Menu(menu_item, "Habits")
    menu.SetXY(20, 50)
    menu.Init()
    #menu_item.HighlightName()
    thread.start_new_thread(BookKeepingThread, ())
    G.screen.GetCharacter()


curses.wrapper(main)
