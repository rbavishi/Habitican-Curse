import curses
from lines_and_text import *
from global_settings import *
from screen_class import *

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
    X=self.x; Y=self.y
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.Highlight("easy", X, Y)
    elif(self.difficulty=="medium"):
      self.screen.Highlight("medium", X, Y+6)
    else:
      self.screen.Highlight("hard", X, Y+14)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)
    




