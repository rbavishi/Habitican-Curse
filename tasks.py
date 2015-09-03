import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
from request_queue import *
import locale
import uuid

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
    self.enqueued      = False
    self.enqPut        = False
    self.changePut     = False
    if(self.value < -20):
      self.color=curses.COLOR_RED+1
    elif(self.value < -10):
      self.color=9
    elif(self.value < -1):
      self.color=8
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    elif(self.value > 5):
      self.color=curses.COLOR_BLUE+2
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y
    self.delete        = False
    self.enqDelete     = False

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

  def MarkUp(self, X, Y):
    if self.up==False:
      return 

    if self.marked==False:
      store=self.TextLine.string
      self.TextLine.string="+"+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.marked=True
      self.mark="up"

      if self.enqueued==False:
	self.enqueued=True
	MANAGER.MarkEnqueue(self)

    else:
      self.marked=False
      self.TextLine.Redefine()
      self.mark=''
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

  def MarkDown(self, X, Y):
    if self.down==False:
      return 

    if self.marked==False:
      store=self.TextLine.string
      self.TextLine.string="-"+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.marked=True
      self.mark="down"

      if self.enqueued==False:
	self.enqueued=True
	MANAGER.MarkEnqueue(self)

    else:
      self.marked=False
      self.TextLine.Redefine()
      self.mark=''
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

  def Delete(self, X, Y):
    if self.delete==False:
      store=self.TextLine.string
      self.TextLine.string="x"+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.delete=True

      if self.enqDelete==False:
	self.enqDelete=True
	MANAGER.DeleteEnqueue(self)

    else:
      self.delete=False
      self.TextLine.Redefine()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

  def ReloadText(self):
    #self.TextLine.string = self.TextLine.string[2:]
    self.TextLine.Redefine()

  def CustomCommand(self, cmd, X, Y):
    if cmd=="set d 0.1" or cmd=="set d trivial":
      if self.difficulty!="trivial":
	self.changePut=True
	self.difficulty="trivial"
	self.json['priority']=0.1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1" or cmd=="set d easy" or cmd=="set d 1.0":
      if self.difficulty!="easy":
	self.changePut=True
	self.difficulty="easy"
	self.json['priority']=1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1.5" or cmd=="set d medium":
      if self.difficulty!="medium":
	self.changePut=True
	self.difficulty="medium"
	self.json['priority']=1.5
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 2" or cmd=="set d hard" or cmd=="set d 2.0":
      if self.difficulty!="hard":
	self.changePut=True
	self.difficulty="hard"
	self.json['priority']=2
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

def WeekToString(wdict):
  s=""
  if wdict['m']==True:
    s+="Mon "
  if wdict['t']==True:
    s+="Tue "
  if wdict['w']==True:
    s+="Wed "
  if wdict['th']==True:
    s+="Thurs "
  if wdict['f']==True:
    s+="Fri "
  if wdict['s']==True:
    s+="Sat "
  if wdict['s']==True:
    s+="Sun "

  return s
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
    self.type_daily    = -1
    if json_dict['frequency']=='daily':
      self.type_daily=json_dict['everyX']
    else:
      self.type_daily=-1

    self.repeat        = json_dict['repeat']
    self.repeat_string = WeekToString(self.repeat)
    self.color         = 0
    self.marked        = False
    self.enqueued      = False
    self.mark          = ''
    self.delete        = False
    self.enqDelete     = False
    self.enqPut        = False
    self.changePut     = False
    if(self.completed==True):
      self.TextLine.string = u'\u2714'.encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()
      #self.TextLine.string = str(json_dict['text'])
    if(self.value < -20):
      self.color=curses.COLOR_RED+1
    elif(self.value < -10):
      self.color=9
    elif(self.value < -1):
      self.color=8
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    elif(self.value > 5):
      self.color=curses.COLOR_BLUE+2
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y

    self.checklist=json_dict['checklist']
    self.orig_checklist=[]
    for i in self.checklist:
      self.orig_checklist+=[i.copy()]
    self.ChecklistObj=Checklist(self.checklist, self.screen, self.TextLine.ColumnText())
    if(self.checklist!=[]):
      self.TextLine.string = u'\u25BC'.encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()

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
    if self.type_daily==-1:
      self.screen.DisplayCustomColorBold("Active Days: ", curses.COLOR_BLUE+2, X, Y)
      self.screen.DisplayCustomColorBold(self.repeat_string, 5, X, Y+15)
    else:
      self.screen.DisplayCustomColorBold("Every ", curses.COLOR_BLUE+2, X, Y)
      self.screen.DisplayCustomColorBold(str(self.type_daily)+" days", 5, X, Y+6)
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

  def ReloadText(self):
    if self.completed==False:
      self.TextLine.string=self.TextLine.string.split(u'\u2714'.encode("utf-8"))[-1][1:]
      self.TextLine.Redefine()

    else:
      self.TextLine.string=(u'\u2714').encode("utf-8")+ " " + self.TextLine.string
      self.TextLine.Redefine()

  def Delete(self, X, Y):
    if self.delete==False:
      store=self.TextLine.string
      self.TextLine.string="x"+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.delete=True

      if self.enqDelete==False:
	self.enqDelete=True
	MANAGER.DeleteEnqueue(self)

    else:
      self.delete=False
      self.TextLine.Redefine()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

  def ShowChecklist(self):
    self.ChecklistObj.Init()
    self.ChecklistObj.Input()
    if self.orig_checklist!=self.ChecklistObj.checklist:
      self.changePut=True
      if self.enqPut==False:
	self.enqPut=True
	MANAGER.PutEnqueue(self)

  def CustomCommand(self, cmd, X, Y):
    if cmd=="set d 0.1" or cmd=="set d trivial":
      if self.difficulty!="trivial":
	self.changePut=True
	self.difficulty="trivial"
	self.json['priority']=0.1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1" or cmd=="set d easy" or cmd=="set d 1.0":
      if self.difficulty!="easy":
	self.changePut=True
	self.difficulty="easy"
	self.json['priority']=1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1.5" or cmd=="set d medium":
      if self.difficulty!="medium":
	self.changePut=True
	self.difficulty="medium"
	self.json['priority']=1.5
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 2" or cmd=="set d hard" or cmd=="set d 2.0":
      if self.difficulty!="hard":
	self.changePut=True
	self.difficulty="hard"
	self.json['priority']=2
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

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
    self.delete        = False
    self.enqDelete     = False
    self.enqPut        = False
    self.changePut     = False
    if(self.value < -20):
      self.color=curses.COLOR_RED+1
    elif(self.value < -10):
      self.color=9
    elif(self.value < -1):
      self.color=8
    elif(self.value < 1):
      self.color=curses.COLOR_YELLOW+1
    elif(self.value > 5):
      self.color=curses.COLOR_BLUE+2
    else:
      self.color=curses.COLOR_GREEN+1

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y

    self.checklist=json_dict['checklist']
    self.orig_checklist=[]
    for i in self.checklist:
      self.orig_checklist+=[i.copy()]
    self.ChecklistObj=Checklist(self.checklist, self.screen, self.TextLine.ColumnText())
    if(self.checklist!=[]):
      self.TextLine.string = u'\u25BC'.encode("utf-8")+" "+self.TextLine.string
      self.TextLine.Redefine()

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

  def Delete(self, X, Y):
    #MyText = self.TextLine.ColumnText()
    if self.delete==False:
      store=self.TextLine.string
      self.TextLine.string="x"+" "+self.TextLine.string
      self.TextLine.Redefine()
      self.TextLine.string=store
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

      self.delete=True

      if self.enqDelete==False:
	self.enqDelete=True
	MANAGER.DeleteEnqueue(self)

    else:
      self.delete=False
      #self.TextLine.string=self.TextLine.string[1:]
      self.TextLine.Redefine()
      self.screen.Highlight(self.TextLine.ColumnText(), X, Y)
      self.screen.screen.refresh()

  def ShowChecklist(self):
    self.ChecklistObj.Init()
    self.ChecklistObj.Input()
    if self.orig_checklist!=self.ChecklistObj.checklist:
      self.changePut=True
      if self.enqPut==False:
	self.enqPut=True
	MANAGER.PutEnqueue(self)

  def CustomCommand(self, cmd, X, Y):
    if cmd=="set d 0.1" or cmd=="set d trivial":
      if self.difficulty!="trivial":
	self.changePut=True
	self.difficulty="trivial"
	self.json['priority']=0.1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1" or cmd=="set d easy" or cmd=="set d 1.0":
      if self.difficulty!="easy":
	self.changePut=True
	self.difficulty="easy"
	self.json['priority']=1
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 1.5" or cmd=="set d medium":
      if self.difficulty!="medium":
	self.changePut=True
	self.difficulty="medium"
	self.json['priority']=1.5
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

    elif cmd=="set d 2" or cmd=="set d hard" or cmd=="set d 2.0":
      if self.difficulty!="hard":
	self.changePut=True
	self.difficulty="hard"
	self.json['priority']=2
	self.Highlight_Title(X, Y)
	if self.enqPut==False:
	  self.enqPut=True
	  MANAGER.PutEnqueue(self)

class ChecklistItem:
  def __init__(self, item, screen, dummy=False, x=0, y=0):
    self.item=item
    self.completed=self.item['completed']
    self.screen=screen
    self.x=x
    self.y=y
    self.dummy=dummy

    self.base_string=str(self.item['text'])
    y,x = self.screen.screen.getmaxyx()
    if len(self.base_string)>(x-17):
      self.base_string=self.base_string[:(x-20)]+"..."

    self.base_string="    "+self.base_string

    self.marked=False
    self.delete=False

  def Toggle(self):
    self.item['completed']=self.item['completed']^True
    self.completed=self.item['completed']

  def ToggleMark(self):
    self.marked=self.marked^True
    self.Highlight()

  def ToggleDelete(self):
    self.delete=self.delete^True
    self.marked=False
    self.Highlight()

  def Display(self):
    if self.completed:
      string = "  "+u'\u2714'.encode("utf-8")+" "+self.base_string[4:]
      if self.delete==True and self.dummy==False:
	string = 'x'+" "+string[2:]
      elif self.marked and self.dummy==False:
	string = u'\u25CF'.encode("utf-8")+" "+string[2:]
      self.screen.Display(string, self.x, self.y)
    else:
      string = self.base_string
      if self.delete==True and self.dummy==False:
	string = 'x'+" "+string[2:]
      elif self.marked and self.dummy==False:
	string = "  "+u'\u25CF'.encode("utf-8")+" "+string[4:]
      self.screen.Display(string, self.x, self.y)

  def Highlight(self):
    if self.completed:
      #string = u'\u2714'.encode("utf-8")+" "+self.base_string
      string = "  "+u'\u2714'.encode("utf-8")+" "+self.base_string[4:]
      if self.delete==True and self.dummy==False:
	string = 'x'+" "+string[2:]
      elif self.marked and self.dummy==False:
	#string = u'\u25CF'.encode("utf-8")+" "+string
	string = u'\u25CF'.encode("utf-8")+" "+string[2:]
      self.screen.Highlight(string, self.x, self.y)
    else:
      string = self.base_string
      if self.delete==True and self.dummy==False:
	string = 'x'+" "+string[2:]
      elif self.marked and self.dummy==False:
	#string = u'\u25CF'.encode("utf-8")+" "+string
	string = "  "+u'\u25CF'.encode("utf-8")+" "+string[4:]
      self.screen.Highlight(string, self.x, self.y)

  def SetXY(self, X, Y):
    self.x=X
    self.y=Y

  def EnterName(self):
    y,x = self.screen.screen.getmaxyx()
    self.screen.Display(" "*(x-1), self.x, self.y)
    curses.echo()
    curses.curs_set(1)
    s=self.screen.screen.getstr(self.x, self.y+4, 50)
    curses.noecho()
    curses.curs_set(0)
    self.item['text']=s
    self.base_string=str(self.item['text'])
    y,x = self.screen.screen.getmaxyx()
    if len(self.base_string)>(x-17):
      self.base_string=self.base_string[:(x-20)]+"..."

    self.base_string="    "+self.base_string
    self.Highlight()


class Checklist:
  def __init__(self, checklist, screen, taskname=''):
    self.checklist=checklist
    self.screen=screen

    self.x=SETTINGS.TASK_WINDOW_X
    self.y=SETTINGS.TASK_WINDOW_Y
    self.taskname=taskname

    self.items=[]
    for i in self.checklist:
      self.items+=[ChecklistItem(i, self.screen)]

    self.AddDummyItem()
    self.counter=0
    self.start=0
    self.end=min(6, len(checklist)+1)


  def Init(self):
    X=self.x
    Y=self.y

    self.screen.Restore()
    self.screen.SaveState()
    self.screen.DisplayCustomColorBold("Checklist - " +self.taskname, 2, X, Y)
    X+=2

    for i in xrange(self.start, self.end):
      self.items[i].SetXY(X, Y)
      X+=1
      self.items[i].Display()

    self.items[self.counter].Highlight()

  def ScrollUp(self):
    if self.counter!=self.start:
      self.items[self.counter].Display()
      self.counter-=1
      self.items[self.counter].Highlight()

    elif self.start!=0:
      self.start-=1
      self.counter-=1
      self.end-=1
      self.Init()

  def ScrollDown(self):
    if self.counter!=(self.end-1):
      self.items[self.counter].Display()
      self.counter+=1
      self.items[self.counter].Highlight()

    elif self.end!=len(self.items):
      self.start+=1
      self.counter+=1
      self.end+=1
      self.Init()

  def AddDummyItem(self):
    new_item={}
    new_item[u'text']=u'Add New Item'
    new_item[u'completed']=False
    new_item[u'id']=str(uuid.uuid4())
    self.items+=[ChecklistItem(new_item, self.screen, True)]

  def Mark(self):
    if self.counter!=(len(self.items)-1):
      self.items[self.counter].ToggleMark()

  def Delete(self):
    if self.counter!=(len(self.items)-1):
      self.items[self.counter].ToggleDelete()

  def EnterName(self):
    self.items[self.counter].EnterName()
    if self.counter == (self.end - 1):
      self.items[self.counter].dummy=False
      self.checklist+=[self.items[self.counter].item]
      self.AddDummyItem()
      self.counter=0
      self.start=0
      self.end=min(6, len(self.checklist)+1)
      self.Init()

  def Input(self):
    while(1):
      c=self.screen.screen.getch()
      if (c==ord('q')):
	for i in self.items:
	  if i.marked==True:
	    i.marked=False
	  if i.delete==True:
	    i.delete=False
	self.screen.Restore()
	self.screen.SaveState()
	break
      elif (c==ord('m')):
	self.Mark()
      elif (c==ord('d')):
	self.Delete()
      elif (c==10):
	self.EnterName()
      elif (c==ord('c')):
	for i in self.items:
	  if i.marked==True:
	    i.Toggle()
	    i.marked=False
	  if i.delete==True:
	    self.checklist.remove(i.item)
	    i.delete=False
	    self.items.remove(i)
	self.screen.Restore()
	self.screen.SaveState()
	break
      elif (c==curses.KEY_UP):
	self.ScrollUp()
      elif (c==curses.KEY_DOWN):
	self.ScrollDown()
      else:
	continue

    




    
	
