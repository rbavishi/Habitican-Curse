import curses
from lines_and_text import *
from global_settings import *
from screen_class import *
from menus import *

#Preliminary Testing of the above code - Press 'q' to quit. Press TAB to toggle.

def main(screen):

  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.init_pair(2, curses.COLOR_RED, -1)
  curses.init_pair(3, curses.COLOR_GREEN, -1)
  curses.init_pair(4, curses.COLOR_YELLOW, -1)
  curses.init_pair(5, curses.COLOR_MAGENTA, -1)
  curses.curs_set(0)

  scr=Screen(screen)

  line=Line(10, 0, "Hello World! I am the stupidest person ever", scr)
  line1=Line(12, 0, "Hello World! I am the stupid", scr)
  scr.Display("Press TAB to toggle 'Hello World!'. Press 'q' to exit")

  while 1:
    c = screen.getch()
    if(c==ord('\t')):
      line.Toggle()
      line1.Toggle()
    elif(c==ord('q')):
      break
    else:
      continue

curses.wrapper(main)



