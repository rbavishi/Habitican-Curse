### Testing Lines and Text

import sys
sys.path.append('../')

import curses
from lines_and_text import *
from screen_class import *
from menus import *
from global_settings import *

def main(screen):

  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.curs_set(0)

  scr=Screen(screen)

  menu_item1 = MenuItem("Item 1", scr)
  menu_item2 = MenuItem("Item 2", scr)
  menu_item3 = MenuItem("Item 3", scr)
  item_list=[menu_item1, menu_item2, menu_item3]

  mymenu = Menu(item_list, "Habits", scr, 10, 10)
  mymenu.Init()

  while 1:
    c = screen.getch()
    if(c==curses.KEY_UP):
      mymenu.ScrollUp()
    elif(c==curses.KEY_DOWN):
      mymenu.ScrollDown()
    elif(c==ord('q')):
      break
    else:
      continue


curses.wrapper(main)
