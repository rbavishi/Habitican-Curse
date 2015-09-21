""" Module "Menu" : Menu classes

    All classes required to implement menus including task menus, chat menus
    etc.
"""

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H

def truncate(string, size):
    return (string[:size-3]+"...") if len(string)>size else string

class MenuItem(object):
    """ A class for storing a single menu item. It will contain the task object
    as well as the status object. It is general enough to be used as a
    checklist item, and an actual task item"""

    def __init__(self, task, task_type, taskname, 
                 width = -1, front = True):
        self.task = task
        self.task_type = task_type

        self.taskname = taskname

        if self.task_type == "habit":
            if self.task.up and self.task.down:
                self.status = H.Status("habit")
            elif self.task.up:
                self.status = H.Status("habitpos")
            elif self.task.down:
                self.status = H.Status("habitneg")
        else:
            self.status = H.Status(self.task_type)

        self.x = 0
        self.y = 0

        # Width specification
        if width == -1:
            self.width = C.SCR_MENU_ITEM_WIDTH
        else:
            self.width = width

        # Should the status be at the front or the back (True/False
        # respectively)
        self.front = front


    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

        if self.front:
            self.status.SetXY(x, y + self.status.ReturnLenString() - 2)
        else:
            self.status.SetXY(x, y + self.width - 1)

    def DisplayName(self, color=0):
        if hasattr(self.task, "color"):
            color = self.task.color

        self.status.Display()
        status_length = self.status.ReturnLenString()
        first_row_size = self.width - status_length - 1

        G.screen.DisplayCustomColorBold(" "*first_row_size, color, self.x,
                                        self.y+status_length+1)
        G.screen.DisplayCustomColorBold(" "*self.width, color, self.x+1,
                                        self.y)
        if hasattr(self.task, 'completed') and self.task.completed:
            G.screen.DisplayCustomColorBold(C.SYMBOL_TICK, color, self.x,
                                            self.y + status_length)
        if len(self.taskname) < first_row_size: # No need to truncate
            if self.front:
                G.screen.DisplayCustomColorBold(self.taskname, color, self.x, self.y +
                                                            status_length + 1)
            else:
                G.screen.DisplayCustomColorBold(self.taskname, color, self.x, self.y)

            G.screen.Display(" "*self.width, self.x+1, self.y)
        else:                                   # We need truncation
            if self.taskname[first_row_size-1] != ' ':
                if self.front:
                    G.screen.DisplayCustomColorBold(self.taskname[:first_row_size-1]+"-",
                                         color, self.x, self.y + status_length + 1)
                else:
                    G.screen.DisplayCustomColorBold(self.taskname[:first_row_size-1]+"-",
                                         color, self.x, self.y)
                G.screen.DisplayCustomColorBold(truncate(self.taskname[first_row_size-1:],
                                              self.width), color,
                                              self.x+1, self.y)
            elif self.taskname[first_row_size-1] == ' ':
                if self.front:
                    G.screen.DisplayCustomColorBold(self.taskname[:first_row_size],
                                         color, self.x, self.y + status_length + 1)
                else:
                    G.screen.DisplayCustomColorBold(self.taskname[:first_row_size],
                                         color, self.x, self.y)
                G.screen.DisplayCustomColorBold(truncate(self.taskname[first_row_size:],
                                              self.width), color,
                                              self.x+1, self.y)

    def HighlightName(self):
        self.status.Display()
        status_length = self.status.ReturnLenString()
        first_row_size = self.width - status_length - 1

        G.screen.Highlight(" "*first_row_size, self.x,
                           self.y+status_length+1)
        G.screen.Highlight(" "*self.width, self.x+1,
                                        self.y)
        if hasattr(self.task, 'completed') and self.task.completed:
            G.screen.Highlight(C.SYMBOL_TICK, self.x,
                                            self.y + status_length)
        if len(self.taskname) < first_row_size:
            if self.front:
                G.screen.Highlight(self.taskname, self.x, self.y +
                                                            status_length + 1)
            else:
                G.screen.Highlight(self.taskname, self.x, self.y)
            G.screen.Highlight(" "*self.width, self.x+1, self.y)
        else:
            if self.taskname[first_row_size-1] != ' ':
                if self.front:
                    G.screen.Highlight(self.taskname[:first_row_size-1]+"-",
                                         self.x, self.y + status_length + 1)
                else:
                    G.screen.Highlight(self.taskname[:first_row_size-1]+"-",
                                         self.x, self.y)
                G.screen.Highlight(truncate(self.taskname[first_row_size-1:],
                                              self.width),
                                              self.x+1, self.y)
            elif self.taskname[first_row_size-1] == ' ':
                if self.front:
                    G.screen.Highlight(self.taskname[:first_row_size],
                                         self.x, self.y + status_length + 1)
                else:
                    G.screen.Highlight(self.taskname[:first_row_size],
                                         self.x, self.y)
                G.screen.Highlight(truncate(self.taskname[first_row_size:],
                                              self.width),
                                              self.x+1, self.y)

    def ToggleMarkUp(self):
        self.status.ToggleMarkUp()
        self.HighlightName()

    def ToggleMarkDown(self):
        self.status.ToggleMarkDown()
        self.HighlightName()

    def ToggleMark(self):
        self.status.ToggleMark()
        self.HighlightName()

    def ToggleDelete(self):
        self.status.ToggleDelete()
        self.HighlightName()

    def ToggleEdit(self):
        self.status.ToggleEdit()
        self.HighlightName()



class Menu(object):
    """ The menu class - For selecting tasks from the interface. General enough
    to be used for tasks as well as checklists"""

    def __init__(self, items, title, rows=-1, menu_type = "task"):
        self.items = items           # Item List
        self.title = title
        self.menu_type = menu_type

        # Defining the menu window using start and end
        if rows == -1:
            rows = C.SCR_MAX_MENU_ROWS
        self.rows = rows

        self.start = 0
        self.end = min(self.rows/2, len(self.items)) 
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
        G.screen.ScrollBar(X, Y-2, self.start, self.end, len(self.items), self.rows)

        for i in xrange(self.start, self.end):
            self.items[i].SetXY(X, Y)
            self.items[i].DisplayName()

            X += 2             # All task items occupy two rows

    def ScrollUp(self):
        if self.start == 0 and self.current == self.start:
            return             # Nothing to do as we've reached the top

        if self.menu_type == "task":
            G.prevTask = G.currentTask

        if self.current != self.start:
            self.current -= 1
            G.currentTask = self.items[self.current]

        else:
            self.start -= 1
            self.current -= 1
            self.end -= 1
            if self.menu_type == "task":
                G.currentTask = self.items[self.current]
            self.Init()       # Reload the menu

    def ScrollDown(self):
        if self.end == len(self.items) and (self.current == self.end - 1):
            return             # Nothing to do as we've reached the bottom

        if self.menu_type == "task":
            G.prevTask = G.currentTask

        if self.current != self.end - 1:
            self.current += 1
            G.currentTask = self.items[self.current]

        else:
            self.start += 1
            self.current += 1
            self.end += 1
            if self.menu_type == "task":
                G.currentTask = self.items[self.current]
            self.Init()       # Reload the menu

    def InitialCurrentTask(self):
        G.prevTask = G.currentTask
        G.currentTask = self.items[self.current]

    def Reload(self):
        self.start = 0
        self.end = min(self.rows/2, len(self.items)) 
        self.current = 0 # Current task number

    def Remove(self, ID):
        for i in self.items:
            if i.task.taskID == ID:
                self.items.remove(i)
                break

    def WriteChanges(self):
        for i in self.items:
            if i.status.attributes.get("+", False):
                G.reqManager.MarkUpQueue.append(i)
                i.status.Reset()
            elif i.status.attributes.get("-", False):
                G.reqManager.MarkDownQueue.append(i)
                i.status.Reset()
            elif i.status.attributes.get(C.SYMBOL_TICK, False):
                G.reqManager.MarkQueue.append(i)
                i.status.Reset()
            elif i.status.attributes.get(C.SYMBOL_DELETE, False):
                G.reqManager.DeleteQueue.append(i)
                i.status.Reset()
            elif i.status.attributes.get(C.SYMBOL_EDIT, False):
                G.reqManager.EditQueue.append(i)
                i.status.Reset()





