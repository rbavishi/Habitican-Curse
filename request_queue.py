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
import tasks as Tasks
from main_interface import *

class Manager:
  def __init__(self):
    self.queue=[]
    self.mark_queue=[]
    self.delete_queue=[]
    self.put_queue=[]

  def Init(self, intf, scr, headers, user_prof):
    self.intf=intf
    self.scr=scr
    self.headers=headers
    self.user_prof=user_prof

  def MarkEnqueue(self, item):
    self.mark_queue+=[item]

  def DeleteEnqueue(self, item):
    self.delete_queue+=[item]

  def PutEnqueue(self, item):
    self.put_queue+=[item]

  def FlushMarks(self):
    drops=[]
    diffdict={}
    diffdict['level']=0; diffdict['hp']=0; diffdict['gp']=0; diffdict['xp']=0; diffdict['mp']=0
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

        new_gp = int(rjson['gp']); new_mp = int(rjson['mp']); new_hp = int(round(rjson['hp'], 0)); new_xp = int(rjson['exp']); new_level=rjson['lvl']
	diffdict['gp']+=new_gp - self.user_prof.gp
	diffdict['hp']+=new_hp - self.user_prof.hp
	diffdict['mp']+=new_mp - self.user_prof.mp
	diffdict['xp']+=new_xp - self.user_prof.exp
	diffdict['level']+=new_level - self.user_prof.level
	self.user_prof.gp=int(rjson['gp'])
	self.user_prof.mp=int(rjson['mp'])
	self.user_prof.hp=int(round(rjson['hp'], 0))
	self.user_prof.exp=int(rjson['exp'])
	self.user_prof.level=rjson['lvl']

	self.user_prof.PrintData()
	self.intf.Init()
	tmp_var=rjson['_tmp']
	if tmp_var.has_key('drop'):
	  if tmp_var['drop'].has_key('dialog'):
	    drops+=[str(tmp_var['drop']['dialog'])]
	  elif tmp_var['drop'].has_key('text'):
	    drops+=[str(tmp_var['drop']['text'])]
	  elif tmp_var['drop'].has_key('notes'):
	    drops+=[str(tmp_var['drop']['notes'])]
    self.mark_queue=[]
    if drops!=[]:
      self.scr.Restore()
      self.scr.SaveState()
      chatmenu=DropMenu(drops, self.scr, SETTINGS.TASK_WINDOW_X, SETTINGS.TASK_WINDOW_Y) 
      chatmenu.Init()
      chatmenu.Input()
      self.scr.Restore()
      self.scr.SaveState()

    self.scr.Restore()
    self.scr.SaveState()
    self.user_prof.PrintGain(diffdict)

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

  def FlushPuts(self):
    for i in self.put_queue:
      if i.changePut==False:
	continue

      i.enqPut=False

      url='https://habitica.com:443/api/v2/user/tasks/'+i.taskID
      resp=requests.put(url, headers=self.headers, json=i.json)
      y,x=self.scr.screen.getmaxyx()
      if resp.status_code==200:
	self.scr.Display(" "*(x-1), y-1, 0)
	self.scr.Display("Successful", y-1, 0)
      else:
	self.scr.Display(" "*(x-1), y-1, 0)
	self.scr.Display("Failed", y-1, 0)

    self.put_queue=[]


  def Flush(self):
    self.FlushPuts()
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
	if quest.has_key('progress') and quest['progress'].has_key('hp'):
	  string ="Boss "+u'\u2665'.encode("utf-8")+" : "+str(int(quest['progress']['hp']))
	  self.scr.DisplayCustomColorBold(string, 2, y-3, 0)
	  self.scr.SaveState()
	elif quest.has_key('progress') and quest['progress'].has_key('collect'):
	  collect_string=""
	  for key, value in quest['progress']['collect'].iteritems():
	    collect_string+=str(key)+" : "+str(value)
	  string ="Collect "+collect_string
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

  def CreateTask(self, task_type):
    string="New "
    if task_type=="todo":
      string+="TODO"
    elif task_type=="daily":
      string+="Daily"
    self.scr.Restore()
    self.scr.SaveState()
    curses.echo()
    curses.curs_set(1)
    self.scr.DisplayBold(string, SETTINGS.TASK_WINDOW_X, SETTINGS.TASK_WINDOW_Y)
    self.scr.Display("Title: ", SETTINGS.TASK_WINDOW_X+2, SETTINGS.TASK_WINDOW_Y)
    s=self.scr.screen.getstr(SETTINGS.TASK_WINDOW_X+2, SETTINGS.TASK_WINDOW_Y + 8, 50)
    curses.noecho()
    curses.curs_set(0)
    if s=="":
      y,x=self.scr.screen.getmaxyx()
      self.scr.Restore()
      self.scr.SaveState()
      self.scr.Display(" "*(x-1), y-1, 0)
      self.scr.Display("Empty Title. Cancelling...", y-1, 0)
      return

    y,x=self.scr.screen.getmaxyx()
    url='https://habitica.com:443/api/v2/user/tasks'
    task={}
    task['text']=s; task['type']=task_type; task['priority']=1
    if task_type=='todo' or task_type=='daily':
      task['checklist']=[]
    self.scr.Display("Creating Task...", y-1, 0)
    resp=requests.post(url, headers=self.headers, json=task)
    if resp.status_code!=200:
      self.scr.Display(" "*(x-1), y-1, 0)
      self.scr.Display("Failed", y-1, 0)
    else:
      self.scr.Restore()
      self.scr.SaveState()
      self.scr.Display(" "*(x-1), y-1, 0)
      self.scr.Display("Successful", y-1, 0)
      json_resp=resp.json()
      if task_type=='todo':
	new_item=MenuItem(Tasks.TODO(json_resp, self.scr), self.scr)
	self.intf.todos=[new_item]+self.intf.todos
	#self.intf.Reload(self.intf.tasks)
	self.intf.Reload()
	self.intf.Init()
      elif task_type=='daily':
	new_item=MenuItem(Tasks.Daily(json_resp, self.scr), self.scr)
	self.intf.dailies=[new_item]+self.intf.dailies
	#self.intf.Reload(self.intf.tasks)
	self.intf.Reload()
	self.intf.Init()
      

  def Refresh(self):
    self.scr.Display("Connecting...")
    f=open('keys.txt', 'r')
    user_id=f.readline().split('\n')[0]
    api_token=f.readline().split('\n')[0]
    headers={'x-api-key':api_token, 'x-api-user':user_id}

    response=requests.get('https://habitica.com:443/api/v2/user/', headers=headers)
    if(response.status_code!=200):
      return 

    #self.scr.screen.clear()
    self.scr.Display("               ")
    self.scr.Display("Connected")
    time.sleep(1)
    self.scr.screen.clear()
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
	  tasks+=[MenuItem(Tasks.Habit(i, self.scr), self.scr)]
	elif i['type']=='daily':
	  tasks+=[MenuItem(Tasks.Daily(i, self.scr), self.scr)]
	elif i['type']=='todo' and i['completed']==False:
	  tasks+=[MenuItem(Tasks.TODO(i, self.scr), self.scr)]
    
    self.intf.Reload(tasks)
    user_prof.Init(self.intf, self.scr, self.headers, resp['stats'])
    self.intf.Init()

MANAGER = Manager()


