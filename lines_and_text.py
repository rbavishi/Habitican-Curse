import curses
from global_settings import *

class Text:
  def __init__(self, string):
    self.string=string
    self.column_string=""
    if len(string) > (COLUMN_TEXT_WIDTH - 1):
      self.column_string=string[:(COLUMN_TEXT_WIDTH - 4)]+"... "
    else:
      self.column_string=string+" "*(COLUMN_TEXT_WIDTH - len(string))

  def RawText(self):
    return self.string

  def ColumnText(self):          ## According to COLUMN_TEXT_WIDTH
    return self.column_string

class Line:
  def __init__(self, x, y, text, screen):
    self.x = x                              # X co-ordinate of starting point
    self.y = y                              # Y co-ordinate of starting point
    self.text = Text(text)                        # Text to be outputted
    self.highlighted=0                      # For toggling the highlighting
    self.screen=screen

  def Display(self):
    self.screen.addstr(self.x, self.y, self.text.ColumnText())
    self.screen.refresh()

  def Highlight(self):
    self.screen.addstr(self.x, self.y, self.text.ColumnText(), curses.color_pair(1)|curses.A_BOLD)
    self.screen.refresh()

  def Toggle(self):
    if self.highlighted==0:
      self.highlighted=1
      self.Highlight()
    else:
      self.highlighted=0
      self.Display()
