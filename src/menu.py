""" Module "Menu" : Menu classes

    All classes required to implement menus including task menus, chat menus
    etc.
"""

# Custom Module Imports

# from import * is bad practice, but we use it just for convenience in case of
# constants
from config import *
from screen import Screen
import global_objects as G
import helper as H

def truncate(string, size):
    return (string[:size-3]+"...") if len(string)>size else string

class MenuItem(object):
    """ A class for storing a single menu item. It will contain the task object
    as well as the status object. """

    def __init__(self, task):
        self.task = task
        self.task_type = "habit"

        self.taskname = "The quick brown fox jumps over the"

        self.status = H.Status(self.task_type)

        self.x = 0
        self.y = 0


    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

        self.status.SetXY(x, y + G.screen.SCR_MENU_ITEM_WIDTH - 1)

    def DisplayName(self):
        self.status.Display()
        status_length = self.status.ReturnLenString()
        first_row_size = G.screen.SCR_MENU_ITEM_WIDTH - status_length

        if len(self.taskname) < first_row_size: # No need to truncate
            G.screen.DisplayBold(self.taskname, self.x, self.y)
            G.screen.Display(" "*G.screen.SCR_MENU_ITEM_WIDTH, self.x+1, self.y)
        else:                                   # We need truncation
            if self.taskname[first_row_size-1]!=' ':
                G.screen.DisplayBold(self.taskname[:first_row_size-1]+"-",
                                     self.x, self.y)
                G.screen.DisplayBold(truncate(self.taskname[first_row_size-1:],
                                              G.screen.SCR_MENU_ITEM_WIDTH),
                                              self.x+1, self.y)
            elif self.taskname[first_row_size-1]==' ':
                G.screen.DisplayBold(self.taskname[:first_row_size]+"-",
                                     self.x, self.y)
                G.screen.DisplayBold(truncate(self.taskname[first_row_size:],
                                              G.screen.SCR_MENU_ITEM_WIDTH),
                                              self.x+1, self.y)

    def HighlightName(self):
        self.status.Display()
        status_length = self.status.ReturnLenString()
        first_row_size = G.screen.SCR_MENU_ITEM_WIDTH - status_length

        if len(self.taskname) < first_row_size:
            G.screen.Highlight(self.taskname, self.x, self.y)
            G.screen.Highlight(" "*G.screen.SCR_MENU_ITEM_WIDTH, self.x+1, self.y)
        else:
            if self.taskname[first_row_size-1] != ' ':
                G.screen.Highlight(self.taskname[:first_row_size-1]+"-",
                                     self.x, self.y)
                G.screen.Highlight(truncate(self.taskname[first_row_size-1:],
                                              G.screen.SCR_MENU_ITEM_WIDTH),
                                              self.x+1, self.y)
            elif self.taskname[first_row_size-1] == ' ':
                G.screen.Highlight(self.taskname[:first_row_size],
                                     self.x, self.y)
                G.screen.Highlight(truncate(self.taskname[first_row_size:],
                                              G.screen.SCR_MENU_ITEM_WIDTH),
                                              self.x+1, self.y)



class Menu(object):
    """ The menu class - For selecting tasks from the interface """

    def __init__(self, items, title):
        self.items = items           # Item List
        self.title = title

        # Defining the menu window using start and end
        self.start = 0
        self.end = min(SCR_MAX_MENU_ROWS/2, len(self.items)) 
        self.current = 0 # Current task number

        # Coordinates
        self.x = 0
        self.y = 0

    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

    def IsEmpty(self):
        if self.items:
            return False
        return True

    def Init(self):
        X, Y = self.x, self.y
        G.screen.DisplayBold(self.title, X, Y)
        X += 2

        for i in xrange(self.start, self.end):
            self.items[i].SetXY(X, Y)
            self.items[i].DisplayName()

            X += 2             # All task items occupy two rows

    def ScrollUp(self):
        if self.start == 0:
            return             # Nothing to do as we've reached the top

        G.prevTask = G.currentTask
        if self.current != self.start:
            self.current -= 1
            G.currentTask = self.items[self.current]

        else:
            self.start -= 1
            self.current -= 1
            self.end -= 1
            G.currentTask = self.items[self.current]
            self.Init()       # Reload the menu

    def ScrollDown(self):
        if self.end == len(self.items):
            return             # Nothing to do as we've reached the bottom

        G.prevTask = G.currentTask
        if self.current != self.end - 1:
            self.current += 1
            G.currentTask = self.items[self.current]

        else:
            self.start += 1
            self.current += 1
            self.end += 1
            G.currentTask = self.items[self.current]
            self.Init()       # Reload the menu


