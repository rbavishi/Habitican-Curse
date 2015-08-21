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

  def Init(self, intf, scr, headers):
    self.intf=intf
    self.scr=scr
    self.headers=headers
    self.queue=[]
    self.mark_queue=[]

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

      i.enqueued=False;

      url='https://habitica.com:443/api/v2/user/tasks/'+i.taskID+"/"+i.mark
      requests.post(url, headers=self.headers)
      self.scr.screen.erase()
      self.intf.Init()
      self.mark_queue=[]

MANAGER = Manager()


