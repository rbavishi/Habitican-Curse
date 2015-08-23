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

class Manager:
  def __init__(self):
    self.queue=[]
    self.mark_queue=[]

  def Init(self, intf, scr, headers, user_prof):
    self.intf=intf
    self.scr=scr
    self.headers=headers
    self.user_prof=user_prof

  def MarkEnqueue(self, item):
    self.mark_queue+=[item]

  def Flush(self):
    for i in self.mark_queue:
      if i.marked==False:
	continue

      i.marked=False
      if i.task_type=="todo":
	for j in xrange(len(self.intf.todos)):
	  if self.intf.todos[j].item.taskID==i.taskID:
	    break
	self.intf.todos.remove(self.intf.todos[j])
	self.intf.TODOMenu.Reload()

      elif i.task_type=="daily":
	i.completed^=True
	i.ReloadText()
     
      elif i.task_type=="habit":
	i.ReloadText()

      i.enqueued=False;

      url='https://habitica.com:443/api/v2/user/tasks/'+i.taskID+"/"+i.mark
      resp=requests.post(url, headers=self.headers)
      rjson=resp.json()
      self.scr.screen.erase()

      self.user_prof.gp=int(rjson['gp'])
      self.user_prof.hp=rjson['hp']
      self.user_prof.exp=rjson['exp']
      self.user_prof.level=rjson['lvl']

      self.user_prof.PrintData()

      self.intf.Init()
      self.mark_queue=[]

MANAGER = Manager()


