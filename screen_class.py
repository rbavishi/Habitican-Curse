import curses
import tempfile

class Screen:

  def __init__(self, screen):
    self.screen=screen
    self.tmpfile=tempfile.TemporaryFile()
    self.stack=[]

  def SaveState(self):
    self.stack.append(self.tmpfile.tell())
    self.screen.putwin(self.tmpfile)

  def Restore(self):
    if len(self.stack)==0:
      return

    self.tmpfile.seek(self.stack[-1])
    self.screen=curses.getwin(self.tmpfile)
    self.screen.refresh()

    removed=self.stack.pop()

  def Display(self, string, x=0, y=0):
    self.screen.addstr(x, y, string)
    self.screen.refresh()

  def DisplayBold(self, string, x=0, y=0):
    self.screen.addstr(x, y, string, curses.A_BOLD)
    self.screen.refresh()

  def Highlight(self, string, x=0, y=0):
    self.screen.addstr(x, y, string, curses.color_pair(1)|curses.A_BOLD)
    self.screen.refresh()

  def DisplayCustomColor(self, string, color=0, x=0, y=0):
    self.screen.addstr(x, y, string, curses.color_pair(color))

  def DisplayCustomColorBold(self, string, color=0, x=0, y=0):
    self.screen.addstr(x, y, string, curses.A_BOLD|curses.color_pair(color))


