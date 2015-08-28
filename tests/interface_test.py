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
#from user import *

user_id=''
api_token=''

locale.setlocale(locale.LC_ALL, '') 

def main(screen):
  global user_prof
  #Colors - Placeholders for now
  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, 19, 244)
  curses.curs_set(0)
  #curses.init_pair(2, curses.COLOR_RED, -1)
  #curses.init_pair(3, curses.COLOR_GREEN, -1)
  #curses.init_pair(4, curses.COLOR_YELLOW, -1)
  #curses.init_pair(5, curses.COLOR_MAGENTA, -1)
  #curses.init_pair(6, curses.COLOR_BLUE, -1)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
  screen.bkgd(' ', curses.color_pair(7))

  scr=Screen(screen)
  scr.Display("Connecting...")

  ### Disable if you want fixed column size
  (y,x)=scr.screen.getmaxyx()
  SETTINGS.COLUMN_TEXT_WIDTH = (x-6)/3

  f=open('keys.txt', 'r')
  user_id=f.readline().split('\n')[0]
  api_token=f.readline().split('\n')[0]
  headers={'x-api-key':api_token, 'x-api-user':user_id}

  response=requests.get('https://habitica.com:443/api/v2/user/', headers=headers)
  if(response.status_code!=200):
    return 

  scr.screen.clear()
  scr.Display("Connected")
  time.sleep(1)
  scr.screen.clear()
  resp=response.json()
  h,d,t = resp['habits'], resp['dailys'], resp['todos']
  if type(h)!=list:
    h=[h]
  if type(d)!=list:
    d=[d]
  if type(t)!=list:
    t=[t]

  tasks=[]
  j=h+d+t

  if(type(j)==list):
    for i in j:
      if i['type']=='habit':
	tasks+=[MenuItem(Habit(i, scr), scr)]
      elif i['type']=='daily':
	tasks+=[MenuItem(Daily(i, scr), scr)]
      elif i['type']=='todo' and i['completed']==False:
	tasks+=[MenuItem(TODO(i, scr), scr)]


  intf = Interface(tasks, scr, MANAGER)
  user_prof.Init(intf, scr, headers, resp['stats'])
  #user_prof.GetStats()
  intf.Init()
  MANAGER.Init(intf, scr, headers, user_prof)
  intf.Input()

  scr.Display("Press q to exit...")
  while 1:
    c = screen.getch()
    if(c==ord('q')):
      break
    else:
      continue


curses.wrapper(main)


