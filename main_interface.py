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


      


