import curses
import tempfile
import global_settings as GLOBAL_SETTINGS

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

  def MenuScrollBar(self, x, y, start, end, length):
    scaled_start=int(round((start*1.0)*(GLOBAL_SETTINGS.SETTINGS.MAX_MENU_ROWS)*(1.0/length)))
    scaled_end=int(round(((end)*1.0)*(GLOBAL_SETTINGS.SETTINGS.MAX_MENU_ROWS)*(1.0/length)))
    #self.Display("st: " + str(scaled_start) + "rows: " + str(GLOBAL_SETTINGS.SETTINGS.MAX_MENU_ROWS)+"length: "+str(length)+"end: " +str(end))
    X = x
    self.DisplayCustomColor(u'\u25B2'.encode("utf-8"), 7, X-1, y) 
    for i in xrange(0, scaled_start):
      self.DisplayCustomColor(" ", 10, X, y)
      X+=1
    for i in xrange(scaled_start, scaled_end):
      self.DisplayCustomColor(" ", 1, X, y)
      X+=1

    for i in xrange(scaled_end, GLOBAL_SETTINGS.SETTINGS.MAX_MENU_ROWS):
      self.DisplayCustomColor(" ", 10, X, y)
      X+=1
    self.DisplayCustomColor(u'\u25BC'.encode("utf-8"), 7, X, y) 





