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
    self.delete_queue=[]

  def Init(self, intf, scr, headers, user_prof):
    self.intf=intf
    self.scr=scr
    self.headers=headers
    self.user_prof=user_prof

  def MarkEnqueue(self, item):
    self.mark_queue+=[item]

  def DeleteEnqueue(self, item):
    self.delete_queue+=[item]

  def FlushMarks(self):
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
      if resp.status_code==200:
	rjson=resp.json()
	self.scr.screen.erase()

	self.user_prof.gp=int(rjson['gp'])
	self.user_prof.hp=rjson['hp']
	self.user_prof.exp=rjson['exp']
	self.user_prof.level=rjson['lvl']

	self.user_prof.PrintData()
	self.intf.Init()
    self.mark_queue=[]

  def FlushDelete(self):
    for i in self.delete_queue:
      if i.delete==False:
	continue

      if i.task_type=="todo":
	for j in xrange(len(self.intf.todos)):
	  if self.intf.todos[j].item.taskID==i.taskID:
	    break
	self.intf.todos.remove(self.intf.todos[j])
	self.intf.TODOMenu.Reload()
	
      elif i.task_type=="daily":
	for j in xrange(len(self.intf.dailies)):
	  if self.intf.dailies[j].item.taskID==i.taskID:
	    break
	self.intf.dailies.remove(self.intf.dailies[j])
	self.intf.DailyMenu.Reload()

      elif i.task_type=="habit":
	for j in xrange(len(self.intf.habits)):
	  if self.intf.habits[j].item.taskID==i.taskID:
	    break
	self.intf.habits.remove(self.intf.habits[j])
	self.intf.HabitMenu.Reload()

      url='https://habitica.com:443/api/v2/user/tasks/'+i.taskID
      resp=requests.delete(url, headers=self.headers)
      if resp.status_code==200:
	self.scr.screen.erase()
	self.user_prof.PrintData()
	self.intf.Init()

    
    self.delete_queue=[]

  def Flush(self):
    self.FlushMarks()
    self.FlushDelete()
    

  def GetPartyData(self):
    resp=requests.get('https://habitica.com/api/v2/groups/party', headers=self.headers)
    y,x=self.scr.screen.getmaxyx()
    if resp.status_code==200:
      rjson=resp.json()
      quest=rjson['quest']
      self.scr.Display(" "*(x-1), y-1, 0)
      self.scr.Display("Done", y-1, 0)
      if quest!={}:
	string ="Boss "+u'\u2665'.encode("utf-8")+" : "+str(int(quest['progress']['hp']))
	self.scr.DisplayCustomColorBold(string, 2, y-3, 0)
	self.scr.SaveState()
  
      chatmenu=ChatMenu(rjson['chat'][:50], self.scr, SETTINGS.TASK_WINDOW_X, SETTINGS.TASK_WINDOW_Y) 
      chatmenu.Init()
      chatmenu.Input()
      if quest!={}:
	self.scr.Restore()

    else:
      self.scr.Display(" "*(x-1), y-1, 0)
      self.scr.Display("Failed", y-1, 0)

MANAGER = Manager()


