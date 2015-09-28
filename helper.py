""" Module "Helper" : Helper functions and classes

    Contains classes and functions for wrapping text, task modification status,
    text menus, date-time etc.
"""

# Standard Library Imports
import time
from datetime import datetime
from dateutil import tz, relativedelta

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import debug as DEBUG
import content as CT


class Status(object):

    def __init__(self, task_type, checklist=[0, 0], due=''):
        if task_type == "habit":
            self.attributes = C.HabitStatus.copy()
        elif task_type == "habitpos":
            self.attributes = C.HabitPosStatus.copy()
        elif task_type == "habitneg":
            self.attributes = C.HabitNegStatus.copy()
        elif task_type == "checklist":
            self.attributes = C.ChecklistStatus.copy()
        else:
            self.attributes = C.TODODailyStatus.copy()
        self.checklist = checklist
        self.due = due
        self.x = 0
        self.y = 0
	self.newItem = False

    def ReturnLenString(self):
        length = 2*len([i for i in self.attributes if self.attributes[i]!=None])
        if self.checklist[1] != 0:
            # (Done/Total) - 4 extra symbols - '(', ')', '/' and a space
            length += 5 + len(str(self.checklist[0])) + len(str(self.checklist[1]))

        if self.due!='':
            length += len(self.due) + 3 # To account for a space

        return length

    def SetXY(self, x=0, y=0):
        self.x = x
        self.y = y

    def SetChecklist(self, checklist):
	self.checklist = checklist

    def Display(self):
        X, Y = self.x, self.y

        if self.checklist[1] != 0:
            display_string = '('+str(self.checklist[0])+'/'+str(self.checklist[1])+')'
            Y -= (len(display_string))
            display_string = C.SYMBOL_DOWN_TRIANGLE + display_string
            G.screen.DisplayCustomColorBold(display_string,
                                            C.SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2

        if self.due != '':
            Y -= (len(self.due) + 1)
            G.screen.DisplayCustomColorBold(C.SYMBOL_DUE + " " + self.due, C.SCR_COLOR_LIGHT_GRAY, X, Y)
            Y -= 2

        for (key, value) in self.attributes.items():
            if value != None:
                if value:
		    G.screen.DisplayCustomColorBold(key, C.SCR_COLOR_YELLOW, X, Y)
                else:
                    G.screen.DisplayCustomColorBold(key, C.SCR_COLOR_DARK_GRAY, X, Y)
                Y -= 2

    def ToggleMarkUp(self):
        # Return if there is no up direction, or the delete option has already
        # been enabled or the edit status is true
        if ((not self.attributes.has_key("+")) or 
            self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes["+"]:
            self.attributes["+"] = False

        else:
            # Only one of "-" and "+" can be activated at a time
            self.attributes["-"] = False
            self.attributes["+"] = True

    def ToggleMarkDown(self):
        # Return if there is no down direction, or the delete option has already
        # been enabled or the edit status is true
        if ((not self.attributes.has_key("-")) or 
            self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes["-"]:
            self.attributes["-"] = False

        else:
            # Only one of "-" and "+" can be activated at a time
            self.attributes["+"] = False
            self.attributes["-"] = True

    def ToggleMark(self):
        # Return if the delete option has already been enabled or the edit
        # status is true
        if (self.attributes[C.SYMBOL_DELETE] or
            self.attributes[C.SYMBOL_EDIT]):
            return

        if self.attributes[C.SYMBOL_TICK]:
            self.attributes[C.SYMBOL_TICK] = False
        else:
            self.attributes[C.SYMBOL_TICK] = True

    def ToggleDelete(self):
        # Nothing can be enabled along with delete
        for key in self.attributes:
            if key != C.SYMBOL_DELETE:
                self.attributes[key] = False

        if self.attributes[C.SYMBOL_DELETE]:
            self.attributes[C.SYMBOL_DELETE] = False
        else:
            self.attributes[C.SYMBOL_DELETE] = True

    def ToggleEdit(self):
        # Return if the delete option has already been enabled or the edit
        # status is true
	if self.attributes[C.SYMBOL_DELETE]:
            return

        for key in self.attributes:
            if key != C.SYMBOL_EDIT:
                self.attributes[key] = False

        if not self.attributes[C.SYMBOL_EDIT]: # Edits cannot be turned "off"
            self.attributes[C.SYMBOL_EDIT] = True

    def Reset(self):
        for key in self.attributes:
            self.attributes[key] = False

	self.newItem = False

    def IsNewItem(self):
	return self.newItem

    def SetNewItem(self):
	self.newItem = True



class DateTime(object):
    """ Class for handling various date-time formats used in Habitica """

    def __init__(self, inpDate=-1):
	if inpDate == -1:
	    inpDate = time.time()*1000
        
        self.date = self.ConvertDate(inpDate)

    def ConvertDate(self, date):
	if type(date) == datetime:
	    return date

        elif type(date) == int or type(date) == float:
            # Milliseconds included in the timestamp
            retDate = datetime.fromtimestamp(date*1.0/1000) 
	    retDate = retDate.replace(tzinfo=tz.tzlocal())

	    return retDate

        elif type(date) == str:
            # UTC Format. We'll convert it to local time.
            # We assume that local time zone can be computed by dateutil
            retDate = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ")

            retDate = retDate.replace(tzinfo=tz.tzutc()) # UTC Time zone convert
            retDate = retDate.astimezone(tz.tzlocal())   # Local Time

            return retDate

    def DueDateFormat(self):
        return self.date.strftime('[%d/%m]')

    def DateCreatedFormat(self):
        # dd-mm-YY format. I'm Indian :)
        return self.date.strftime('%d/%m/%Y')


def GetDifferenceTime(d2, d1=-1): # d1 - d2
    Date1 = DateTime(d1)
    Date2 = DateTime(d2)
    #DEBUG.Display(Date1.DueDateFormat())
    #time.sleep(20)


    diffDate = relativedelta.relativedelta(Date1.date, Date2.date)
    if diffDate.years!=0:
        return str(diffDate.years)+'y ago'
    if diffDate.months!=0:
        return str(diffDate.months)+'months ago'
    if diffDate.days!=0:
        return str(diffDate.days)+'d ago'
    if diffDate.hours!=0:
        return str(diffDate.hours)+'h ago'

    return str(diffDate.minutes)+'m ago'


def isDueDaily(task):
    if task['frequency'] == 'weekly':
	translateDict = {0: 'm', 1: 't', 2: 'w', 3: 'th', 4: 'f', 5: 's', 6: 'su'}
	if task['repeat'][translateDict[datetime.today().weekday()]]:
	    return True
	else:
	    return False

    elif task['frequency'] == 'daily':
	startDate = DateTime(str(task['startDate']))
	current   = DateTime(-1)
	diffDay   = (current.date - startDate.date).days
	if diffDay % (task['everyX']) == 0:
	    return True
	else:
	    return False

    return False


def GetUserStats(data):
    stats = data['stats']
    gear  = data['items']['gear']['equipped']
    userClass = stats['class']

    # Intelligence
    statInt = (stats['int'] +            # Allocated
    	      stats['buffs']['int'] +    # Buffed
	      min(stats['lvl'],100)/2)   # Level Bonus

    for i in gear.values():
	gearStats = G.content.Equipment(i)
	if ((gearStats['klass'] == userClass) or 
		(gearStats['klass'] == "special" and gearStats['specialClass'] == userClass)):
	       statInt += gearStats['int']*1.5
	else:
	    statInt += gearStats['int']

    # Perception
    statPer = (stats['per'] +            # Allocated
    	       stats['buffs']['per'] +   # Buffed
	       min(stats['lvl'],100)/2)  # Level Bonus

    for i in gear.values():
	gearStats = G.content.Equipment(i)
	if ((gearStats['klass'] == userClass) or 
		(gearStats['klass'] == "special" and gearStats['specialClass'] == userClass)):
	       statPer += gearStats['per']*1.5
	else:
	    statPer += gearStats['per']

    # Strength
    statStr = (stats['str'] +            # Allocated
    	       stats['buffs']['str'] +   # Buffed
	       min(stats['lvl'],100)/2)  # Level Bonus

    for i in gear.values():
	gearStats = G.content.Equipment(i)
	if ((gearStats['klass'] == userClass) or 
		(gearStats['klass'] == "special" and gearStats['specialClass'] == userClass)):
	       statStr += gearStats['str']*1.5
	else:
	    statStr += gearStats['str']

    # Constitution
    statCon = (stats['con'] +            # Allocated
    	       stats['buffs']['con'] +   # Buffed
	       min(stats['lvl'],100)/2)  # Level Bonus

    for i in gear.values():
	gearStats = G.content.Equipment(i)
	if ((gearStats['klass'] == userClass) or 
		(gearStats['klass'] == "special" and gearStats['specialClass'] == userClass)):
	       statCon += gearStats['con']*1.5
	else:
	    statCon += gearStats['con']

    if statInt == int(statInt):
	statInt = int(statInt)

    if statStr == int(statStr):
	statStr = int(statStr)

    if statPer == int(statPer):
	statPer = int(statPer)

    if statCon == int(statCon):
	statCon = int(statCon)

    return {'int': statInt, 'per': statPer, 'str': statStr, 'con': statCon}

