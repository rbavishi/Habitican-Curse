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
  menu_item4 = MenuItem("Item 4", scr)
  menu_item5 = MenuItem("Item 5", scr)
  menu_item6 = MenuItem("Item 6", scr)
  menu_item7 = MenuItem("Item 7", scr)
  menu_item8 = MenuItem("Item 8", scr)
  menu_item9 = MenuItem("Item 9", scr)
  menu_item10 = MenuItem("Item 10", scr)
  menu_item11 = MenuItem("Item 11", scr)
  menu_item12 = MenuItem("Item 12", scr)
  menu_item13 = MenuItem("Item 13", scr)
  item_list=[menu_item1, menu_item2, menu_item3, menu_item4, menu_item5, menu_item6, menu_item7, menu_item8, menu_item9, menu_item10, menu_item11, menu_item12, menu_item13]

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
