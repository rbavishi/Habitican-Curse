import curses
from lines_and_text import *
from global_settings import *
from screen_class import *

class MenuItem:
  def __init__(self, item, screen):
    self.item=item
    self.task_type=item.task_type
    self.screen=screen
    self.x=0
    self.y=0

  def SetXY(self, x, y):
    self.x=x
    self.y=y

  def Display(self, x=0, y=0, restore=True):
    self.item.Display_Title(self.x, self.y, restore)

  def Highlight(self, x=0, y=0, show=True):
    self.item.Highlight_Title(self.x, self.y, show)

  def Enter(self):
    a = 10 ## Placeholder

  def Mark(self):
    if self.item.task_type=='habit':
      return
    else:
      self.item.Mark(self.x, self.y)

  def MarkUp(self):
    if self.item.task_type!='habit':
      return
    self.item.MarkUp(self.x, self.y)

  def MarkDown(self):
    if self.item.task_type!='habit':
      return
    self.item.MarkDown(self.x, self.y)


class Menu:
  def __init__(self, item_list, title, screen, x=0, y=0):
    self.items=item_list
    self.screen=screen
    self.title=Line(x, y, title, screen)
    self.x=x
    self.y=y
    self.counter=0
    if(len(item_list)==0):
      self.counter=-1
    self.start=0
    self.end=min(SETTINGS.MAX_MENU_ROWS-1, len(item_list)-1)

  def Init(self, highlight=True):
    self.title.DisplayBold()
    new_x=self.x + 2

    for i in xrange(self.start, self.end+1):
      item=self.items[i]
      item.SetXY(new_x, self.y)
      item.Display(restore=False)
      new_x+=1

    self.screen.SaveState()
    if highlight==True and self.counter!=-1:
      self.items[self.counter].Highlight(False)

    self.screen.screen.refresh()

  def NoHighlight(self):
    if self.counter==-1:
      return

    self.items[self.counter].Display()
    self.screen.screen.refresh()

  def Highlight(self):
    self.items[self.counter].Highlight()
    self.screen.screen.refresh()

  def ScrollUp(self):
    if self.counter==self.start and self.start==0:
      return

    elif self.counter==self.start:
      self.screen.Restore()
      self.screen.SaveState()
      self.start-=1
      self.end-=1
      self.counter-=1
      self.Init()
      self.screen.screen.refresh()

    else:
      self.items[self.counter].Display()
      self.counter-=1
      self.items[self.counter].Highlight()
      self.screen.screen.refresh()

  def ScrollDown(self):
    if self.counter==self.end and self.end==(len(self.items)-1):
      return

    elif self.counter==self.end:
      self.screen.Restore()
      self.screen.SaveState()
      self.end+=1
      self.start+=1
      self.counter+=1
      self.Init()
      self.screen.screen.refresh()

    else:
      self.items[self.counter].Display()
      self.counter+=1
      self.items[self.counter].Highlight()
      self.screen.screen.refresh()

  def IsEmpty(self):
    return len(self.items)==0

  def Mark(self):
    self.items[self.counter].Mark()

  def MarkUp(self):
    self.items[self.counter].MarkUp()

  def MarkDown(self):
    self.items[self.counter].MarkDown()

  def Reload(self):
    if(len(self.items)==0):
      self.counter=-1
    self.start=0
    self.end=min(SETTINGS.MAX_MENU_ROWS-1, len(self.items)-1)

class ChatItem:
  def __init__(self, text, width):
    self.text=text
    self.width=width-5

    self.text_strings=['  '+text[i:i+self.width] for i in xrange(0, len(text), self.width)]
    #self.text_strings[0]=u'\u25CF'.encode("utf-8")+self.text_strings[0][1:]
    self.text_strings[0]="*"+self.text_strings[0][1:]



class ChatMenu:
  def __init__(self, item_list, screen, x=0, y=0):
    self.x=x
    self.y=y

    self.screen=screen
    self.item_list=[i['text'] for i in item_list]

    Y,X=screen.screen.getmaxyx()
    self.text_strs=[]
    for i in self.item_list:
      j=ChatItem(i, X)
      self.text_strs+=j.text_strings+['-'*(X-15)]

    self.start=0
    self.end=min(Y-20, len(self.text_strs))

  def Init(self):
    if self.end<=0:
      return
    X=self.x
    Y=self.y

    for i in xrange(self.start, self.end):
      self.screen.DisplayBold(self.text_strs[i], X, Y)
      X+=1

  def ScrollUp(self):
    if self.start!=0:
      self.screen.Restore()
      self.screen.SaveState()
      self.start-=1
      self.end-=1
      self.Init()

  def ScrollDown(self):
    if self.end!=len(self.text_strs):
      self.screen.Restore()
      self.screen.SaveState()
      self.end+=1
      self.start+=1
      self.Init()

  def Input(self):
    while(1):
      c=self.screen.screen.getch()
      if(c==curses.KEY_UP or c==ord('k') ):
	self.ScrollUp()
      elif(c==curses.KEY_DOWN or c==ord('j')):
	self.ScrollDown()
      elif(c==ord('q')):
	break










