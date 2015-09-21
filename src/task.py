""" Module "Task" : Classes for storing task information

    The python class version of the model described on the github page of
    Habitica.
"""

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H


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


class Task(object):
    """ Basic template for a task. There will be separate derived classes for
    Habits, TODOs and Dailies """

    def __init__(self, data):
        self.data = data          # JSON response received from request

        # Basic Details
        self.text        = str(data['text'])
        self.taskID      = str(data['id'])
        self.dateCreated = str(data['dateCreated']).split('T')[0]
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


class Habit(Task):
    """ Class for holding a habit """

    def __init__(self, data):
        super(Habit, self).__init__(data)
        self.task_type = "habit"
        self.up   = data['up']
        self.down = data['down']


class Daily(Task):
    """ Class for holding a daily """

    def __init__(self, data):
        self.task_type = "daily"
        super(Daily, self).__init__(data)


class TODO(Task):
    """ Class for holding a habit """

    def __init__(self, data):
        self.task_type = "todo"
        super(TODO, self).__init__(data)
