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

    self.HabitMenu=Menu(self.habits, "Habits", screen, 2, 1)
    self.DailyMenu=Menu(self.dailies, "Dailies", screen, 2, 3+SETTINGS.COLUMN_TEXT_WIDTH)
    self.TODOMenu =Menu(self.todos,  "TODOs", screen, 2, 5+2*SETTINGS.COLUMN_TEXT_WIDTH)

    self.current=0

  def Init(self):
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
    s=self.screen.screen.getstr(y-1, 1)
    curses.noecho()
    if(s=="w"):
      self.screen.Display("Connecting...", y-1, 0)
      self.manager.Flush()
      self.screen.Display(" "*(x-1), y-1, 0)
      self.screen.Display("Done", y-1, 0)

    elif(s=="boss"):
      self.screen.Restore()
      self.screen.SaveState()
      self.screen.Display("Connecting...", y-1, 0)
      self.manager.GetPartyData()

    else:
      self.screen.Display(" "*(x-1), y-1, 0)



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

    self.hp        = j['hp']
    self.gp        = int(j['gp'])
    self.maxHP     = j['maxHealth']
    self.exp       = j['exp']
    self.req_exp   = j['toNextLevel']
    self.level     = j['lvl']
    self.PrintData()

  def GetStats(self):
    y,x=self.scr.screen.getmaxyx()
    self.scr.Display("Fetching User Data...", y-1, 0)
    resp=requests.get('https://habitica.com:443/api/v2/user/', headers=self.headers)
    j=resp.json()['stats']
    self.scr.Display(" "*(x-1), y-1, 0)

    self.hp        = j['hp']
    self.gp        = int(j['gp'])
    self.maxHP     = j['maxHealth']
    self.exp       = j['exp']
    self.req_exp   = j['toNextLevel']
    self.level     = j['lvl']


    self.PrintData()

  def PrintData(self):
    y,x=self.scr.screen.getmaxyx()
    #Level
    string =u'\u2949'.encode("utf-8")+" "+str(self.level)+" "
    self.scr.DisplayCustomColorBold(string, 0, y-2, 0)
    
    #Health
    string =u'\u2665'.encode("utf-8")+" "+str(self.hp)+"/"+str(self.maxHP)+" "
    self.scr.DisplayCustomColorBold(string, 2, y-2, 6) 

    #Experience
    string =u'\u2605'.encode("utf-8")+" "+str(self.exp)+"/"+str(self.req_exp)+" "
    self.scr.DisplayCustomColorBold(string, 3, y-2, 17)

    #Gold
    string =u'\u25CF'.encode("utf-8")+" "+str(self.gp)
    self.scr.DisplayCustomColorBold(string, 4, y-2, 29)




user_prof = UserClass()
      


