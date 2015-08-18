import curses
from lines_and_text import *
from global_settings import *
from screen_class import *

class MenuItem:
  def __init__(self, text, screen):
    self.text=Text(text)
    self.screen=screen
    self.x=0
    self.y=0

  def SetXY(self, x, y):
    self.x=x
    self.y=y

  def Display(self, x=0, y=0):
    self.screen.Display(self.text.ColumnText(), self.x, self.y)

  def Highlight(self, x=0, y=0):
    self.screen.Highlight(self.text.ColumnText(), self.x, self.y)

  def Enter(self):
    a = 10 ## Placeholder


class Menu:
  def __init__(self, item_list, title, screen, x=0, y=0):
    self.items=item_list
    self.screen=screen
    self.title=Line(x, y, title, screen)
    self.x=x
    self.y=y
    self.counter=0

  def Init(self):
    self.title.DisplayBold()
    new_x=self.x + 2

    for i in self.items:
      i.SetXY(new_x, self.y)
      i.Display()
      new_x+=1

    self.items[self.counter].Highlight()

  def NoHighlight(self):
    if self.counter==-1:
      return

    self.items[self.counter].Display()
    self.counter=-1

  def ScrollUp(self):
    if self.counter==0:
      return

    else:
      self.items[self.counter].Display()
      self.counter-=1
      self.items[self.counter].Highlight()

  def ScrollDown(self):
    if self.counter==(len(self.items)-1):
      return

    else:
      self.items[self.counter].Display()
      self.counter+=1
      self.items[self.counter].Highlight()





