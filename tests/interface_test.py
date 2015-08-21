### Testing Interface -  Store user-ID and api-token in the file keys.txt in the tests folder

import sys
import time
import locale
sys.path.append('../')

import curses
import requests
from lines_and_text import *
from screen_class import *
from menus import *
from global_settings import *
from tasks import *
from main_interface import *

user_id=''
api_token=''

locale.setlocale(locale.LC_ALL, '') 

def main(screen):
  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.curs_set(0)
  curses.init_pair(2, curses.COLOR_RED, -1)
  curses.init_pair(3, curses.COLOR_GREEN, -1)
  curses.init_pair(4, curses.COLOR_YELLOW, -1)
  curses.init_pair(5, curses.COLOR_MAGENTA, -1)

  scr=Screen(screen)
  scr.Display("Connecting...")

  ### Disable if you want fixed column size
  (y,x)=scr.screen.getmaxyx()
  SETTINGS.COLUMN_TEXT_WIDTH = (x-6)/3

  f=open('keys.txt', 'r')
  user_id=f.readline().split('\n')[0]
  api_token=f.readline().split('\n')[0]
  headers={'x-api-key':api_token, 'x-api-user':user_id}

  response=requests.get('https://habitica.com:443/api/v2/user/tasks', headers=headers)
  if(response.status_code!=200):
    return 

  scr.screen.clear()
  scr.Display("Connected")
  time.sleep(1)
  scr.screen.clear()
  j=response.json()
  if type(j)!=list:
    j=[j]

  tasks=[]

  if(type(j)==list):
    for i in j:
      if i['type']=='habit':
	tasks+=[MenuItem(Habit(i, scr), scr)]
      elif i['type']=='daily':
	tasks+=[MenuItem(Daily(i, scr), scr)]
      elif i['type']=='todo' and i['completed']==False:
	tasks+=[MenuItem(TODO(i, scr), scr)]


  intf = Interface(tasks, scr, MANAGER)
  intf.Init()
  MANAGER.Init(intf, scr, headers)
  intf.Input()

  scr.Display("Press q to exit...")
  while 1:
    c = screen.getch()
    if(c==ord('q')):
      break
    else:
      continue


curses.wrapper(main)


