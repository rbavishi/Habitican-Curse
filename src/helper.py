""" Module "Helper" : Helper functions and classes

    Contains classes and functions for wrapping text, task modification status,
    text menus etc.
"""

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G


class Status(object):

    def __init__(self, task_type, checklist=[0, 0], due=''):
        if task_type == "habit":
            self.attributes = C.HabitStatus.copy()
        elif task_type == "habitpos":
            self.attributes = C.HabitPosStatus.copy()
        elif task_type == "habitneg":
            self.attributes = C.HabitNegStatus.copy()
        elif task_type == "checklist":
            self.attributes = C.ChecklistStatus.copy()
        else:
            self.attributes = C.TODODailyStatus.copy()
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
                    G.screen.DisplayCustomColorBold(key, C.SCR_COLOR_CYAN, X, Y)
                else:
                    G.screen.DisplayCustomColorBold(key, C.SCR_COLOR_DARK_GRAY, X, Y)
                Y -= 2

        if self.checklist[1] != 0:
            display_string = '('+str(self.checklist[0])+'/'+str(self.checklist[1])+')'
            Y -= (len(display_string) - 1)
            G.screen.DisplayCustomColorBold(display_string,
                                            C.SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2

        if self.due != '':
            Y -= (len(self.due) - 1)
            G.screen.DisplayCustomColorBold(self.due, C.SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2

    def ToggleMarkUp(self):
        # Return if there is no up direction, or the delete option has already
        # been enabled or the edit status is true
        if ((not self.attributes.has_key("+")) or 
            self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes["+"]:
            self.attributes["+"] = False

        else:
            # Only one of "-" and "+" can be activated at a time
            self.attributes["-"] = False
            self.attributes["+"] = True

    def ToggleMarkDown(self):
        # Return if there is no down direction, or the delete option has already
        # been enabled or the edit status is true
        if ((not self.attributes.has_key("-")) or 
            self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes["-"]:
            self.attributes["-"] = False

        else:
            # Only one of "-" and "+" can be activated at a time
            self.attributes["+"] = False
            self.attributes["-"] = True

    def ToggleMark(self):
        # Return if the delete option has already been enabled or the edit
        # status is true
        if (self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes[C.SYMBOL_TICK]:
            self.attributes[C.SYMBOL_TICK] = False
        else:
            self.attributes[C.SYMBOL_TICK] = True

    def ToggleDelete(self):
        # Nothing can be enabled along with delete
        for key in self.attributes:
            if key != C.SYMBOL_DELETE:
                self.attributes[key] = False

        if self.attributes[C.SYMBOL_DELETE]:
            self.attributes[C.SYMBOL_DELETE] = False
        else:
            self.attributes[C.SYMBOL_DELETE] = True

    def Reset(self):
        for key in self.attributes:
            self.attributes[key] = False

