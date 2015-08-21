import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
from request_queue import *
import locale

class Habit:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='habit'
    self.up            = json_dict['up']
    self.down          = json_dict['down']
    self.text          = str(json_dict['text'])
    self.TextLine      = Text(self.text)
    diff               = {0.1:'trivial', 1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.color         = 0
    self.mark          = 'up'
    self.marked        = False
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y

  def Init(self):

    X=self.x; Y=self.y
    self.screen.DisplayBold("Habit", X, Y)
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("trivial  easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y+9)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+15)
    elif(self.difficulty=="hard"):
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+23)
    else:
      self.screen.DisplayCustomColorBold("trivial", 5, X, Y)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)

  def Display_Title(self, X, Y, restore=True):
    if restore==True:
      self.screen.Restore()
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)
      self.screen.SaveState()
    else:
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)
      

  def Highlight_Title(self, X, Y, show=True):
    if show==True:
      self.screen.Restore()
      self.screen.SaveState()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.Init()
    else:
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)

  def Mark(self, X, Y):
    MyText = self.TextLine.ColumnText()
    if self.marked==False:
      MyText=(u'\u25CF').encode("utf-8")+" "+MyText[:-1]
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)

      self.marked=True
      self.mark='up'

      if self.enqueued==False:
	self.enqueued=True
	MANAGER.MarkEnqueue(self)

    else:
      self.marked=False
      MyText+=" "
      self.mark='down'
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)

class Daily:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='daily'
    self.text          = str(json_dict['text'])
    self.TextLine      = Text(self.text)
    diff               = {0.1:'trivial', 1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.completed     = json_dict['completed']
    self.color         = 0
    self.marked        = False
    self.enqueued      = False
    self.mark          = ''
    if(self.completed==True):
      self.TextLine.string = u'\u2714'.encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()
      #self.TextLine.string = str(json_dict['text'])
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y

  def Init(self):

    X=self.x; Y=self.y
    completed_string=u''
    if self.completed==True:
      completed_string=u'\u2714'
    self.screen.DisplayBold("Daily " + completed_string.encode("utf-8"), X, Y)
    self.screen.screen.refresh()
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("trivial  easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y+9)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+15)
    elif(self.difficulty=="hard"):
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+23)
    else:
      self.screen.DisplayCustomColorBold("trivial", 5, X, Y)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)
    
  def Display_Title(self, X, Y, restore=True):
    if restore==True:
      self.screen.Restore()
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)
      self.screen.SaveState()
    else:
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)


  def Highlight_Title(self, X, Y, show=True):
    if show==True:
      self.screen.Restore()
      self.screen.SaveState()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.Init()
    else:
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)

  def Mark(self, X, Y):
    #MyText = self.TextLine.ColumnText()
    if self.marked==False:
      store=self.TextLine.string
      self.TextLine.string=(u'\u25CF').encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.marked=True
      if self.completed==True:
	self.mark='down'
      else:
	self.mark='up'

      if self.enqueued==False:
	self.enqueued=True
	MANAGER.MarkEnqueue(self)

    else:
      self.marked=False
      self.TextLine.Redefine()
      self.mark=''
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

class TODO:
  def __init__(self, json_dict, screen):
    self.json=json_dict
    self.screen=screen

    self.task_type='todo'
    self.text          = str(json_dict['text'])
    self.TextLine      = Text(self.text)
    diff               = {0.1:'trivial', 1:'easy', 1.5:'medium', 2:'hard'}
    self.difficulty    = diff[json_dict['priority']]
    self.taskID        = str(json_dict['id'])
    self.dateCreated   = str(json_dict['dateCreated']).split('T')[0]
    self.value         = json_dict['value']
    self.color         = 0
    self.mark          = 'up'
    self.marked        = False
    self.enqueued      = False
    if(self.value < -1):
      self.color=curses.COLOR_RED+1
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y

  def Init(self):
    X=self.x; Y=self.y
    self.screen.DisplayBold("TODO", X, Y)
    X+=3
    self.screen.DisplayCustomColorBold(self.text, self.color, X, Y)

    X+=2
    self.screen.DisplayBold("trivial  easy  medium  hard", X, Y)
    if(self.difficulty=="easy"):
      self.screen.DisplayCustomColorBold("easy", 5, X, Y+9)
    elif(self.difficulty=="medium"):
      self.screen.DisplayCustomColorBold("medium", 5, X, Y+15)
    elif(self.difficulty=="hard"):
      self.screen.DisplayCustomColorBold("hard", 5, X, Y+23)
    else:
      self.screen.DisplayCustomColorBold("trivial", 5, X, Y)

    X+=2
    self.screen.Display("Date Created: "+self.dateCreated, X, Y)

  def Display_Title(self, X, Y, restore=True):
    if restore==True:
      self.screen.Restore()
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)
      self.screen.SaveState()
    else:
      self.screen.DisplayCustomColorBold(self.TextLine.ColumnText(), self.color, X, Y)

  def Highlight_Title(self, X, Y, show=True):
    if show==True:
      self.screen.Restore()
      self.screen.SaveState()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.Init()
    else:
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)

  def Mark(self, X, Y):
    #MyText = self.TextLine.ColumnText()
    if self.marked==False:
      store=self.TextLine.string
      self.TextLine.string=(u'\u25CF').encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.marked=True
      self.mark='up'

      if self.enqueued==False:
	self.enqueued=True
	MANAGER.MarkEnqueue(self)

    else:
      self.marked=False
      #self.TextLine.string=self.TextLine.string[1:]
      self.TextLine.Redefine()
      self.mark=''
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

	
