""" Module "Task" : Classes for storing task information

    The python class version of the model described on the github page of
    Habitica.
"""
# Standard Library Imports
import textwrap

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H
import menu as M


def ValueToColor(value):
    if value < -20:
      return C.SCR_COLOR_RED
    elif value < -10:
      return C.SCR_COLOR_DARK_ORANGE
    elif value < -1:
      return C.SCR_COLOR_LIGHT_ORANGE
    elif value < 1:
      return C.SCR_COLOR_YELLOW
    elif value < 5:
      return C.SCR_COLOR_GREEN
    else:
      return C.SCR_COLOR_BLUE


def PriorityToDifficulty(priority):
    if priority == 0.1:
        return "trivial"
    elif priority == 1:
        return "easy"
    elif priority == 1.5:
        return "medium"
    else:
        return "hard"

def RepeatToString(repeat):
    Translate = {'m': 'Mon', 't': 'Tue', 'th': 'Thurs', 'w': 'Wed', 's':'Sat', 'su': 'Sun', 'f': 'Fri'}
    TranslateOrder = ['m', 't', 'w', 'th', 'f', 's', 'su']
    retString = ""
    for i in TranslateOrder:
        if repeat[i]:
            retString += Translate[i] + " "

    return retString

def ChecklistMenu(checklist):
    if not checklist:
	return None

    checklist_items = []
    for i in checklist:
	task_item = ChecklistItem(i)
	checklist_items += [M.MenuItem(task_item, 'checklist', task_item.text, width=(C.SCR_Y-20))]

    menuObj = M.Menu(checklist_items, 'Checklist', (C.SCR_X - (C.SCR_MAX_MENU_ROWS+7+4+2)), 'checklist_menu')
    menuObj.SetXY(C.SCR_MAX_MENU_ROWS+7, 5)
    return menuObj


class Task(object):
    """ Basic template for a task. There will be separate derived classes for
    Habits, TODOs and Dailies. Basic display facilities are described in the 
    display function of this class. Other details are displayed by the 
    function in the derived classes
    """

    def __init__(self, data):
        self.data = data          # JSON response received from request

        # Basic Details
        self.text        = str(data['text'])
        self.taskID      = str(data['id'])
        self.dateCreated = H.DateTime(str(data['dateCreated']))
        self.priority    = data['priority']
        self.value       = data['value']

        # Derived Details
        self.color       = ValueToColor(self.value)
        self.difficulty  = PriorityToDifficulty(self.priority)

        # Coordinates for displaying complete details
        self.x           = 0
        self.y           = 0

    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

    def Display(self):
        #G.screen.RestoreRegister(0)
        G.screen.ClearTextArea()
        X, Y = self.x, self.y

        # Title Display
        title_wrap = textwrap.wrap(self.text, C.SCR_Y-20)
        for i in title_wrap:
            G.screen.DisplayCustomColorBold(i+'\n', self.color, X, Y)
            X += 1
        X += 1

        # Difficulty
        G.screen.DisplayBold("Difficulty: ", X, Y)
        G.screen.DisplayCustomColorBold(self.difficulty, C.SCR_COLOR_MAGENTA, X, Y+12)
        X += 2

        # Date Created
        G.screen.DisplayBold("Date Created: ", X, Y)
        G.screen.DisplayCustomColorBold(self.dateCreated.DateCreatedFormat(),
                                        C.SCR_COLOR_MAGENTA, X, Y+14)
        X += 2

        return X


class ChecklistItem(object):
    """ Class for holding a checklist item """
    
    def __init__(self, data):

	# Checklist Item Specifications
	self.text      = str(data['text'])
	self.completed = data['completed']
	self.ID        = str(data['id'])

    def Display(self): # Dummy
	return


class Habit(Task):
    """ Class for holding a habit """

    def __init__(self, data):
        super(Habit, self).__init__(data)
        self.task_type = "habit"

        # Special Attributes
        self.up   = data['up']
        self.down = data['down']

    def Display(self):
        X = super(Habit, self).Display()
        Y = self.y

        # Something can be added here
        # Maybe use the data-display tool


class Daily(Task):
    """ Class for holding a daily """

    def __init__(self, data):
        self.task_type = "daily"
        super(Daily, self).__init__(data)

        # Special Attributes
        self.completed = data['completed']
        self.checklist = data['checklist']

        self.frequency = data['frequency']
        self.repeat    = data['repeat']
        self.everyX    = data['everyX']

	# Checklist Menu. None if it is empty
	self.checklistMenu = ChecklistMenu(self.checklist)

    def ChecklistTuple(self):  # Return (done/total)
        done = len([i for i in self.checklist if i['completed']])
        total = len(self.checklist)
        return [done, total]

    def Display(self):
        X = super(Daily, self).Display()
        Y = self.y

        if self.frequency == "daily": # Every X days
            G.screen.DisplayCustomColorBold("Every " + str(self.everyX) + " days", C.SCR_COLOR_MAGENTA, X, Y)
        else:                         # Active on some days of the week
            G.screen.DisplayCustomColorBold("Active: " + RepeatToString(self.repeat), C.SCR_COLOR_MAGENTA, X, Y)
        X += 2

        # Checklist
        if self.checklist:
            done, total = self.ChecklistTuple()
            G.screen.DisplayCustomColorBold("Checklist: " + "("+str(done)+"/"+str(total)+")" + " completed", 
                                             C.SCR_COLOR_MAGENTA, X, Y)
            X += 2

    def ShowChecklist(self):
	if self.checklistMenu == None:
	    return

	G.screen.ClearTextArea()
	self.checklistMenu.Init()
	self.checklistMenu.Input()


class TODO(Task):
    """ Class for holding a habit """

    def __init__(self, data):
        self.task_type = "todo"
        super(TODO, self).__init__(data)

        # Special Attributes
        self.completed = data['completed']
        self.checklist = data['checklist']

        if data.has_key('date'): # Due Date Stuff
            self.dueDate = H.DateTime(str(data['date'])).DueDateFormat()
            self.date    = str(data['date'])
        else:
            self.dueDate = ""
            self.date    = ""

	# Checklist Menu. None if it is empty
	self.checklistMenu = ChecklistMenu(self.checklist)

    def ChecklistTuple(self):  # Return (done/total)
        done = len([i for i in self.checklist if i['completed']])
        total = len(self.checklist)
        return [done, total]

    def Display(self):
        X = super(TODO, self).Display()
        Y = self.y

        # Due Date
        if self.date != "":
            G.screen.DisplayCustomColorBold("Due: " + H.DateTime(self.date).DateCreatedFormat(),
                                            C.SCR_COLOR_MAGENTA, X, Y)
            X += 2

        # Checklist
        if self.checklist:
            done, total = self.ChecklistTuple()
            G.screen.DisplayCustomColorBold("Checklist: " + "("+str(done)+"/"+str(total)+")" + " completed", 
                                             C.SCR_COLOR_MAGENTA, X, Y)
            X += 2

    def ShowChecklist(self):
	if self.checklistMenu == None:
	    return

	G.screen.ClearTextArea()
	self.checklistMenu.Init()
	self.checklistMenu.Input()
