import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
import locale

class Habit:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='habit'
    self.up            = json_dict['up']
    self.down          = json_dict['down']
    self.text          = str(json_dict['text'])
    diff               = {1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.color         = 0
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=TASK_WINDOW_X
    self.y=TASK_WINDOW_Y

  def Init(self):
    box = curses.newwin(8, max(20, len(self.text)+4, len(self.dateCreated)+18), self.x+2, self.y-2)
    box.box()
    self.screen.screen.refresh()
    box.refresh()

    X=self.x; Y=self.y
    self.screen.DisplayBold("Habit", X, Y)
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+6)
    else:
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+14)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)

class Daily:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='daily'
    self.text          = str(json_dict['text'])
    diff               = {1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.completed     = json_dict['completed']
    self.color         = 0
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=TASK_WINDOW_X
    self.y=TASK_WINDOW_Y

  def Init(self):
    box = curses.newwin(8, max(20, len(self.text)+4, len(self.dateCreated)+18), self.x+2, self.y-2)
    box.box()
    self.screen.screen.refresh()
    box.refresh()

    X=self.x; Y=self.y
    completed_string=u''
    if self.completed==True:
      completed_string=u'\u2174'
    self.screen.DisplayBold("Daily " + u'\u2714'.encode("utf-8"), X, Y)
    self.screen.screen.refresh()
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+6)
    else:
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+14)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)
    

class TODO:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='todo'
    self.text          = str(json_dict['text'])
    diff               = {1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.color         = 0
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=TASK_WINDOW_X
    self.y=TASK_WINDOW_Y

  def Init(self):
    box = curses.newwin(8, max(20, len(self.text)+4, len(self.dateCreated)+18), self.x+2, self.y-2)
    box.box()
    self.screen.screen.refresh()
    box.refresh()

    X=self.x; Y=self.y
    self.screen.DisplayBold("TODO", X, Y)
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+6)
    else:
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+14)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)


