import curses
from lines_and_text import *
from global_settings import *

#Preliminary Testing of the above code - Press 'q' to quit. Press TAB to toggle.

def main(screen):

  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.curs_set(0)

  line=Line(10, 0, "Hello World! I am the stupidest person ever", screen)
  line1=Line(12, 0, "Hello World! I am the stupid", screen)
  screen.addstr("Press TAB to toggle 'Hello World!'. Press 'q' to exit")

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



