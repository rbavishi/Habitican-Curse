import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
from menus import *
from request_queue import *

class Interface:
  def __init__(self, tasks, screen, manager):
    self.screen=screen
    self.tasks=tasks
    self.manager=manager

    self.habits=[]
    self.dailies=[]
    self.todos=[]

    for i in tasks:
      if i.task_type=="habit":
	self.habits+=[i]

      elif i.task_type=="daily":
	self.dailies+=[i]

      else:
	self.todos+=[i]

    self.HabitMenu=Menu(self.habits, "Habits", screen, 2, 2)
    self.DailyMenu=Menu(self.dailies, "Dailies", screen, 2, 5+SETTINGS.COLUMN_TEXT_WIDTH)
    self.TODOMenu =Menu(self.todos,  "TODOs", screen, 2, 8+2*SETTINGS.COLUMN_TEXT_WIDTH)

    self.current=0

  def Reload(self):
    self.tasks=self.habits+self.dailies+self.todos

    self.habits=[]
    self.dailies=[]
    self.todos=[]

    for i in self.tasks:
      if i.task_type=="habit":
	self.habits+=[i]

      elif i.task_type=="daily":
	self.dailies+=[i]

      else:
	self.todos+=[i]

    self.HabitMenu=Menu(self.habits, "Habits", self.screen, 2, 2)
    self.DailyMenu=Menu(self.dailies, "Dailies", self.screen, 2, 5+SETTINGS.COLUMN_TEXT_WIDTH)
    self.TODOMenu =Menu(self.todos,  "TODOs", self.screen, 2, 8+2*SETTINGS.COLUMN_TEXT_WIDTH)

  def Init(self):
    y,x=self.screen.screen.getmaxyx()
    self.screen.DisplayCustomColorBold('='*(x-1), 7, 13, 0)
    self.DailyMenu.Init(False)
    self.TODOMenu.Init(False)
    self.HabitMenu.Init()

  def IntfScrollUp(self):
    if self.current==0:
      self.HabitMenu.ScrollUp()
    elif self.current==1:
      self.DailyMenu.ScrollUp()
    else:
      self.TODOMenu.ScrollUp()

  def IntfScrollDown(self):
    if self.current==0:
      self.HabitMenu.ScrollDown()
    elif self.current==1:
      self.DailyMenu.ScrollDown()
    else:
      self.TODOMenu.ScrollDown()

  def IntfScrollLeft(self):
    if self.current==0:
      return

    else:
      if self.current==1 and self.HabitMenu.IsEmpty()==False:
	self.DailyMenu.NoHighlight()
	self.HabitMenu.Highlight()
	self.current-=1

      elif self.current==2 and (self.HabitMenu.IsEmpty()==False or self.DailyMenu.IsEmpty()==False):
	self.TODOMenu.NoHighlight()
	if self.DailyMenu.IsEmpty()==True:
	  self.HabitMenu.Highlight()
	  self.current=0
	else:
	  self.DailyMenu.Highlight()
	  self.current=1
 
  def IntfScrollRight(self):
    if self.current==2:
      return

    else:
      if self.current==1 and self.TODOMenu.IsEmpty()==False:
	self.DailyMenu.NoHighlight()
	self.TODOMenu.Highlight()
	self.current+=1

      elif self.current==0 and (self.DailyMenu.IsEmpty()==False or self.TODOMenu.IsEmpty()==False):
	self.HabitMenu.NoHighlight()
	if self.DailyMenu.IsEmpty()==True:
	  self.TODOMenu.Highlight()
	  self.current=2
	else:
	  self.DailyMenu.Highlight()     
	  self.current=1

  def Mark(self):
    if self.current==0:
      return
    elif self.current==1:
      self.DailyMenu.Mark()
    else:
      self.TODOMenu.Mark()

  def Delete(self):
    if self.current==0:
      self.HabitMenu.Delete()
    elif self.current==1:
      self.DailyMenu.Delete()
    else:
      self.TODOMenu.Delete()

  def ShowChecklist(self):
    #if self.current==0:
      #self.HabitMenu.Delete()
    if self.current==1:
      self.DailyMenu.ShowChecklist()
      self.DailyMenu.Highlight()
    elif self.current==2:
      self.TODOMenu.ShowChecklist()
      self.TODOMenu.Highlight()

  def HabitPlus(self):
    if self.current!=0:
      return

    self.HabitMenu.MarkUp()

  def HabitMinus(self):
    if self.current!=0:
      return

    self.HabitMenu.MarkDown()


  def Input(self):
    while(1):
      c=self.screen.screen.getch()
      if(c==curses.KEY_UP or c==ord('k') ):
	self.IntfScrollUp()
      elif(c==curses.KEY_DOWN or c==ord('j')):
	self.IntfScrollDown()
      elif(c==curses.KEY_LEFT or c==ord('h')):
	self.IntfScrollLeft()
      elif(c==curses.KEY_RIGHT or c==ord('l')):
	self.IntfScrollRight()
      elif(c==ord('m')):
	self.Mark()
      elif(c==ord('c')):
	self.ShowChecklist()
      elif(c==ord('d')):
	self.Delete()
      elif(c==ord('+')):
	self.HabitPlus()
      elif(c==ord('-')):
	self.HabitMinus()
      elif(c==ord(':')):
	self.Command()
      elif(c==ord('q')):
	break
      else:
	continue

  def Command(self):
    y,x=self.screen.screen.getmaxyx()
    self.screen.Display(" "*(x-1), y-1, 0)
    self.screen.Display(":", y-1, 0)
    curses.echo()
    curses.curs_set(1)
    s=self.screen.screen.getstr(y-1, 1).strip()
    curses.curs_set(0)
    curses.noecho()
    if(s=="w"):
      self.screen.Display("Connecting...", y-1, 0)
      self.manager.Flush()
      self.screen.Display(" "*(x-1), y-1, 0)
      self.screen.Display("Done", y-1, 0)

    elif(s=="quest"):
      self.screen.Restore()
      self.screen.SaveState()
      self.screen.Display("Connecting...", y-1, 0)
      self.manager.GetPartyData()

    elif(s=="r"):
      self.manager.Refresh()

    elif(s=="et"):
      self.manager.CreateTask('todo')

    elif(s=="ed"):
      self.manager.CreateTask('daily')

    else:
      self.screen.Display(" "*(x-1), y-1, 0)
      if self.current==0:
	self.HabitMenu.CustomCommand(s)
      elif self.current==1:
	self.DailyMenu.CustomCommand(s)
      else:
	self.TODOMenu.CustomCommand(s)




class UserClass:
  def __init__(self):
    self.a=0
    
  def Init(self, intf, scr, headers, j):
    self.intf=intf
    self.headers=headers
    self.scr=scr

    self.hp=0
    self.gp=0
    self.exp=0
    self.req_exp=0
    self.maxHP=0
    self.level=0

    self.hp        = int(round(j['hp'], 0))
    self.gp        = int(j['gp'])
    self.maxHP     = j['maxHealth']
    self.mp        = int(j['mp'])
    self.maxMP     = int(j['maxMP'])
    self.exp       = int(j['exp'])
    self.req_exp   = int(j['toNextLevel'])
    self.level     = j['lvl']
    self.PrintData()

  def GetStats(self):
    y,x=self.scr.screen.getmaxyx()
    self.scr.Display("Fetching User Data...", y-1, 0)
    resp=requests.get('https://habitica.com:443/api/v2/user/', headers=self.headers)
    j=resp.json()['stats']
    self.scr.Display(" "*(x-1), y-1, 0)

    self.hp        = int(round(j['hp'], 0))
    self.gp        = int(j['gp'])
    self.mp        = int(j['mp'])
    self.maxMP     = int(j['maxMP'])
    self.maxHP     = j['maxHealth']
    self.exp       = int(j['exp'])
    self.req_exp   = int(j['toNextLevel'])
    self.level     = j['lvl']


    self.PrintData()

  def PrintData(self):
    y,x=self.scr.screen.getmaxyx()
    #Level
    string =u'\u2949'.encode("utf-8")+" "+str(self.level)+" "
    self.scr.DisplayCustomColorBold(string, 0, y-2, 0)
    
    #Health
    string =u'\u2665'.encode("utf-8")+" "+str(self.hp)+"/"+str(self.maxHP)+" "
    self.scr.DisplayCustomColorBold(string, 2, y-2, 7) 

    #Experience
    string =u'\u2605'.encode("utf-8")+" "+str(self.exp)+"/"+str(self.req_exp)+" "
    self.scr.DisplayCustomColorBold(string, 3, y-2, 17)

    #Gold
    string =u'\u25CF'.encode("utf-8")+" "+str(self.gp)+" "
    self.scr.DisplayCustomColorBold(string, 4, y-2, 28)

    #MP
    string =u'\u2600'.encode("utf-8")+" "+str(self.mp)+"/"+str(self.maxMP)+" "
    self.scr.DisplayCustomColorBold(string, 6, y-2, 35) 

  def PrintGain(self, diffdict):
    y,x=self.scr.screen.getmaxyx()
    Y=1
    #Level
    if diffdict['level']!=0:
      string =u'\u2949'.encode("utf-8")+" "+('{0:+d}'.format(diffdict['level']))+" "
      self.scr.DisplayCustomColorBold(string, 0, y-3, 0)
      Y+=7
    
    #Health
    if diffdict['hp']!=0:
      string =u'\u2665'.encode("utf-8")+" "+('{0:+d}'.format(diffdict['hp']))+" "
      self.scr.DisplayCustomColorBold(string, 2, y-3, 7) 
      Y+=7

    #Experience
    if diffdict['xp']!=0:
      string =u'\u2605'.encode("utf-8")+" "+('{0:+d}'.format(diffdict['xp']))+" "
      self.scr.DisplayCustomColorBold(string, 3, y-3, 17)
      Y+=7

    #Gold
    if diffdict['gp']!=0:
      string =u'\u25CF'.encode("utf-8")+" "+('{0:+d}'.format(diffdict['gp']))+" "
      self.scr.DisplayCustomColorBold(string, 4, y-3, 28)
      Y+=7

    #MP
    if diffdict['mp']!=0:
      string =u'\u2600'.encode("utf-8")+" "+('{0:+d}'.format(diffdict['mp']))+" "
      self.scr.DisplayCustomColorBold(string, 6, y-3, 35)
      Y+=7



user_prof = UserClass()
      


