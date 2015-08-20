import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
from menus import *

class Interface:
  def __init__(self, tasks, screen):
    self.screen=screen
    self.tasks=tasks

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
    self.DailyMenu=Menu(self.dailies, "Dailies", screen, 2, 3+COLUMN_TEXT_WIDTH)
    self.TODOMenu =Menu(self.todos,  "TODOs", screen, 2, 5+2*COLUMN_TEXT_WIDTH)

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

  def Input(self):
    while(1):
      c=self.screen.screen.getch()
      if(c==curses.KEY_UP):
	self.IntfScrollUp()
      elif(c==curses.KEY_DOWN):
	self.IntfScrollDown()
      elif(c==curses.KEY_LEFT):
	self.IntfScrollLeft()
      elif(c==curses.KEY_RIGHT):
	self.IntfScrollRight()

      elif(c==ord('q')):
	break
      else:
	continue


      


