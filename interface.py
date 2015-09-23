""" Module "Interface" : Main Interface

    Command parsing, menu positioning etc.
"""
# Standard Library Imports
import curses

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H
import menu as M
import request_manager as RM
import debug as DEBUG


class Interface(object):
    
    def __init__(self):
        self.trinity = []
        self.currentMenu = 0

    def Init(self):
        G.HabitMenu.SetXY(1, 2)
        G.DailyMenu.SetXY(1, 6 + C.SCR_MENU_ITEM_WIDTH)
        G.TODOMenu.SetXY(1, 10 + 2*C.SCR_MENU_ITEM_WIDTH)

        G.HabitMenu.Reload()
        G.DailyMenu.Reload()
        G.TODOMenu.Reload()

        G.HabitMenu.Init()
        G.DailyMenu.Init()
        G.TODOMenu.Init()

        # Borders
        G.screen.DisplayCustomColorBold("="*C.SCR_Y, C.SCR_COLOR_WHITE, 14, 0)

        # User Stats
        G.user.PrintData()

        # Save this context for future use in a register
        G.screen.SaveInRegister(0)
        G.screen.SaveInRegister(3) # For storing marks and deletes

        # Used for scrolling
        self.trinity = [G.HabitMenu, G.DailyMenu, G.TODOMenu]
        self.currentMenu = 0
        for i in xrange(0, 3):
            if not self.trinity[i].IsEmpty():
                self.currentMenu = i
                break
        self.trinity[self.currentMenu].InitialCurrentTask()
        self.Highlight()

    def Highlight(self):
        if G.prevTask != None:
            G.prevTask.DisplayName()

        G.currentTask.HighlightName()

    def ScrollUp(self):
        self.trinity[self.currentMenu].ScrollUp()
        self.Highlight()

    def ScrollDown(self):
        self.trinity[self.currentMenu].ScrollDown()
        self.Highlight()

    def ScrollLeft(self):
        if self.currentMenu == 0: # Very Annoying otherwise
            return

        for i in [(self.currentMenu-1)%3, (self.currentMenu-2)%3,
                self.currentMenu]:
            if not self.trinity[i].IsEmpty():
                break
        self.currentMenu = i
        self.trinity[self.currentMenu].InitialCurrentTask()
        self.Highlight()

    def ScrollRight(self):
        if self.currentMenu == 2: # Very annoying otherwise
            return 
        for i in [(self.currentMenu+1)%3, (self.currentMenu+2)%3,
                self.currentMenu]:
            if not self.trinity[i].IsEmpty():
                break
        self.currentMenu = i
        self.trinity[self.currentMenu].InitialCurrentTask()
        self.Highlight()

    # For marking habits as "+"
    def ToggleMarkUp(self):
        if self.currentMenu != 0:
            return

        G.currentTask.ToggleMarkUp()
        G.currentTask.HighlightName()

    # For marking habits as "-"
    def ToggleMarkDown(self):
        if self.currentMenu != 0:
            return

        G.currentTask.ToggleMarkDown()
        G.currentTask.HighlightName()

    # For marking tasks and dailies as completed
    def ToggleMark(self):
        if self.currentMenu == 0:
            return

        G.currentTask.ToggleMark()
        G.currentTask.HighlightName()

    # For marking tasks for deletion
    def ToggleDelete(self):

        G.currentTask.ToggleDelete()
        G.currentTask.HighlightName()

    # Display Checklist
    def Checklist(self):
	G.screen.SaveInRegister(1)
	G.currentTask.ShowChecklist()
	G.screen.RestoreRegister(1)

    def Command(self, command):
        if command == "w":
            G.prevTask = None
            G.currentTask = None

            G.HabitMenu.WriteChanges()
            G.DailyMenu.WriteChanges()
            G.TODOMenu.WriteChanges()
            G.reqManager.Flush()

        elif command == "r":
            G.prevTask = None
            G.currentTask = None

            G.reqManager.FetchData()
            G.screen.Erase()
            self.Init()
        
        elif command == "party":
            G.screen.SaveInRegister(1)
            G.user.GetPartyData()
            G.screen.RestoreRegister(1)

	elif command == "data-display":
	    G.reqManager.DataDisplayTool()

	else:
	    DEBUG.Display("Invalid: " + command)

    def Input(self):
        while(1):
            c = G.screen.GetCharacter()
            if c == curses.KEY_UP:
                self.ScrollUp()
            elif c == curses.KEY_DOWN:
                self.ScrollDown()
            elif c == curses.KEY_LEFT:
                self.ScrollLeft()
            elif c == curses.KEY_RIGHT:
                self.ScrollRight()
            elif c == ord('m'):
                self.ToggleMark()
            elif c == ord('d'):
                self.ToggleDelete()
            elif c == ord('+'):
                self.ToggleMarkUp()
            elif c == ord('-'):
                self.ToggleMarkDown()
	    elif c == ord('c'):
		self.Checklist()
            elif c == ord(':'):
                command = G.screen.Command()

                # Vim style exit
                if command == "q":
                    break 

                G.screen.Display(" "*(C.SCR_Y-1), C.SCR_X-1, 0)
                self.Command(command)
