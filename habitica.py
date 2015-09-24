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
    while(G.screen == None):
        i = 2
    i = 2
    while(1):
        G.screen.Display(str(i))
        i += 1
        time.sleep(2)

def ContentFetchThread():
    G.content = CT.ContentManager()

def main(curses_screen):
    G.screen = Screen(curses_screen)
    G.screen.Initialize()
    C.ConfigureRuntime(curses_screen)
    G.reqManager = RM.RequestManager() 
    G.reqManager.FetchData()
    G.intf = I.Interface()
    G.intf.Init()
    thread.start_new_thread(ContentFetchThread, ())

    G.intf.Input()

    #G.screen.GetCharacter()


curses.wrapper(main)
