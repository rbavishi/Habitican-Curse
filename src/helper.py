""" Module "Helper" : Helper functions and classes

    Contains classes and functions for wrapping text, task modification status,
    text menus etc.
"""

# Custom Module Imports

# from import * is bad practice, but we use it just for convenience in case of
# constants
from config import *
from screen import Screen
import global_objects as G


class Status(object):

    def __init__(self, task_type, checklist=[0, 0], due=''):
        if task_type == "habit":
            self.attributes = HabitStatus.copy()
        elif task_type == "habitpos":
            self.attributes = HabitPosStatus.copy()
        elif task_type == "habitneg":
            self.attributes = HabitNegStatus.copy()
        else:
            self.attributes = TODODailyStatus.copy()
        self.checklist = checklist
        self.due = due
        self.x = 0
        self.y = 0

    def ReturnLenString(self):
        length = 2*len([i for i in self.attributes if self.attributes[i]!=None])
        if self.checklist[1] != 0:
            # (Done/Total) - 4 extra symbols - '(', ')', '/' and a space
            length += 4 + len(str(self.checklist[0])) + len(str(self.checklist[1]))

        if self.due!='':
            length += len(self.due) + 1 # To account for a space

        return length

    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

    def Display(self):
        X, Y = self.x, self.y
        for (key, value) in self.attributes.items():
            if value != None:
                if value:
                    G.screen.DisplayCustomColorBold(key, SCR_COLOR_CYAN, X, Y)
                else:
                    G.screen.DisplayCustomColorBold(key, SCR_COLOR_DARK_GRAY, X, Y)
                Y -= 2

        if self.checklist[1] != 0:
            display_string = '('+str(self.checklist[0])+'/'+str(self.checklist[1])+')'
            Y -= (len(display_string) - 1)
            G.screen.DisplayCustomColorBold(display_string,
                                            SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2

        if self.due != '':
            Y -= (len(self.due) - 1)
            G.screen.DisplayCustomColorBold(self.due, SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2
