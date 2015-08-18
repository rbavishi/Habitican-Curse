### Testing Lines and Text

import sys
sys.path.append('../')

import curses
from lines_and_text import *
from screen_class import *

def main(screen):

  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.curs_set(0)

  scr=Screen(screen)

  line=Line(10, 0, "Hello World!", scr)
  scr.Display("Press TAB to toggle 'Hello World!'. Press 'q' to exit")

  while 1:
    c = screen.getch()
    if(c==ord('\t')):
      line.Toggle()
    elif(c==ord('q')):
      break
    else:
      continue


curses.wrapper(main)
