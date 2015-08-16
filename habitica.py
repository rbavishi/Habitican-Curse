import curses
screen = curses.initscr()

#Initialization
curses.noecho()
curses.cbreak()
screen.keypad(True)

#Colors - Placeholders for now
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

class Line:
  def __init__(self, x, y, text):
    self.x = x                              # X co-ordinate of starting point
    self.y = y                              # Y co-ordinate of starting point
    self.text = text                        # Text to be outputted
    self.highlighted=0                      # For toggling the highlighting

  def Display(self):
    screen.addstr(self.x, self.y, self.text)
    screen.refresh()

  def Highlight(self):
    screen.addstr(self.x, self.y, self.text, curses.color_pair(1))
    screen.refresh()

  def Toggle(self):
    if self.highlighted==0:
      self.highlighted=1
      self.Highlight()
    else:
      self.highlighted=0
      self.Display()

#Preliminary Testing of the above code - Press 'q' to quit. Press TAB to toggle.

line=Line(10, 0, "Hello World!")
screen.addstr("Press TAB to toggle 'Hello World!'. Press 'q' to exit")

while 1:
  c = screen.getch()
  if(c==ord('\t')):
    line.Toggle()
  elif(c==ord('q')):
    break
  else:
    continue

curses.nocbreak()
screen.keypad(0)
curses.echo()

curses.endwin()




