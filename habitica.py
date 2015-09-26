""" Module "Habitica" : Main Driver Program

    The main program is launched from this module
"""
# Standard Library Imports
import curses
import tempfile
import time
import locale
import threading

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H
import menu as M
import request_manager as RM
import interface as I
import content as CT

user_id = ''
api_token = ''

# Ability to display symbols
locale.setlocale(locale.LC_ALL, '') 

def BookKeepingThread():
    G.content = CT.ContentManager()

    # Set user stats now that content has been fetched
    G.user.attrStats = H.GetUserStats(G.user.data)
    G.user.PrintUserStats()

def main(curses_screen):
    G.screen = Screen(curses_screen)
    G.screen.Initialize()
    C.ConfigureRuntime(curses_screen)
    G.reqManager = RM.RequestManager() 
    G.reqManager.FetchData()
    G.intf = I.Interface()
    G.intf.Init()
    bookThread = threading.Thread(target=BookKeepingThread)
    bookThread.start()
    #inputThread = threading.Thread(target=G.intf.Input)
    #inputThread.start()


    G.intf.Input()


curses.wrapper(main)
