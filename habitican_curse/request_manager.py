""" Module "Request Manager" : Module for interacting via Habitica API

    All fetching, scoring, editing, deleting activities are defined here.
"""
# Standard Library Imports
import requests
import time
import imp
import importlib
import datetime

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H
import menu as M
import task as T
import debug as DEBUG
import user as U

# URL Definitions
API_URL = dict()
API_URL['base']    = "https://habitica.com:443/api/v3"
API_URL['user']    = API_URL['base']+"/user"
API_URL['task']    = API_URL['base']+"/tasks"
API_URL['content'] = API_URL['base']+"/content"
API_URL['party']   = API_URL['base']+"/groups/party"

#Request Methods
request_methods = dict()
request_methods['get'] = requests.get
request_methods['post'] = requests.post
request_methods['delete'] = requests.delete


class RequestManager(object):
    """ The main class for sending/receiving data to the habitica server """

    def __init__(self):

        self.headers = {'x-api-key': C.getConfig("key"), 'x-api-user': C.getConfig("uuid")}
        self.ClearQueues()

    # Flush Queues
    def ClearQueues(self):

        self.MarkUpQueue = []
        self.MarkDownQueue = []
        self.MarkQueue = []
        self.DeleteQueue = []
        self.EditQueue = []

    # General Wrapper to fetch JSON data from server
    def FetchJSON(self,kind,params='',failure='hard',method='get'):

        if kind not in API_URL:
            raise ValueError("Unknown API type ",kind)
        if method not in request_methods:
            raise ValueError("Unknown Method type ",method)

        url = API_URL[kind]+"/"+params
        DEBUG.logging.warn("Requesting JSON from %s" % url)
        resp = request_methods[method](url, headers=self.headers)

        # Need some error handling here
        if resp.status_code!=200:
            if(failure=='hard'):
                raise ValueError("HTTP Response not 'okay': %d" % resp.status_code)
            else:
                DEBUG.logging.warn("HTTP Response not 'okay': %d" % resp.status_code)
                rval = -1
        else:
            rval = resp.json()['data']

        #DEBUG.logging.debug("USER JSON Response -\n %s" % str( rval ) )
        return rval

    #Fetches basic user data for the interface
    def FetchData(self):


        G.LastUpdate = datetime.datetime.now()

        #Get the user data from the API
        DEBUG.Display("Connecting...")

        user_json = self.FetchJSON('user')
        task_json = self.FetchJSON('task',params='user')

        DEBUG.Display("Connected")
        time.sleep(1)
        DEBUG.Display(" ")


        # Initialize User Stats
        G.user = U.User( user_json )

        # These will contain the menu items passed to create the Habit, Daily
        # and Todo menus
        habit_items   = []
        dailies_items = []
        todos_items   = []

        DEBUG.logging.debug("Found %d tasks" % len(task_json))

        for i in task_json:
            i['dateCreated'] = i['createdAt'] #TODO: Fix this V2->V3 hack

            DEBUG.logging.debug("Processing a TODO: %s" % str(i['text']))
            if( i['type'] == "habit" ):
                item = T.Habit(i)
                habit_items += [M.MenuItem(item, "habit", item.text)]
            elif( i['type'] == "daily" ):
                item = T.Daily(i)
                dailies_items += [M.MenuItem(item, "daily", item.text)]
            elif( i['type'] == "todo" ):
                if i['completed']:
                    continue
                item = T.TODO(i)
                todos_items += [M.MenuItem(item, "todo", item.text)]
            else:
                raise ValueError("Unknown task type %s" % i['type'])

        # Generate the menus for the display
        G.HabitMenu = M.Menu(habit_items, "Habits")
        G.DailyMenu = M.Menu(dailies_items, "Dailies")
        G.TODOMenu  = M.Menu(todos_items, "TODOs")


    # Write back changes to the server and update the interface
    def Flush(self):

        #TODO: most of this should not happen in the request manager
        import content as CT

        DEBUG.Display("Please Wait...")

        Drops = list()

        # Difference obtained in user stats due to these operations
        origDict = {'hp': G.user.hp, 'gp': G.user.gp, 'mp': G.user.mp,
                    'exp': G.user.exp, 'lvl': G.user.lvl}
        diffDict = origDict.copy()

        #
        #
        #
        # Habits marked as +
        for i in self.MarkUpQueue:
            DEBUG.logging.debug("Marking '%s' up" % str(i.taskname))
            json = self.FetchJSON('task',params=i.task.taskID + "/score/up",method='post')

            for i in diffDict:
                diffDict[i] = json[i]

            # Check for drops
            tmpdrp = CT.CheckDrops( json['_tmp'] )
            if( tmpdrp is not None):
                Drops.append(tmpdrp)

        #
        #
        #
        # Habits marked as -
        for i in self.MarkDownQueue:
            DEBUG.logging.debug("Marking '%s' down" % str(i))
            json = self.FetchJSON('task',                               \
                                  params=i.task.taskID + "/score/down", \
                                  method='post')
            for i in diffDict:
                diffDict[i] = json[i]

        #
        #
        #
        # Dailies and TODOS marked as completed
        for i in self.MarkQueue:
            direction = None
            if i.task.task_type != "daily" or (not i.task.completed):
                direction = "up"
                #URL = GET_TASKS_URL + "/" + i.task.taskID + "/" + "up"
            else:
                direction = "down"
                #URL = GET_TASKS_URL + "/" + i.task.taskID + "/" + "down"

            if (direction is None):
                continue

            json = self.FetchJSON('task',                               \
                                  params=i.task.taskID + "/score/" + direction, \
                                  method='post')

            if i.task.task_type == "todo":
                G.TODOMenu.Remove(i.task.taskID)
            elif i.task.task_type == "daily":
                i.task.completed ^= True

	    for i in diffDict:
		diffDict[i] = json[i]

            # Check for drops
            tmpdrp = CT.CheckDrops( json['_tmp'] )
            if( tmpdrp is not None):
                Drops.append(tmpdrp)

        #
        #
        #
        #for i in self.DeleteQueue:
        # TODO: Needs to be updated to V3 API
        if(False):
            URL = GET_TASKS_URL + "/" + i.task.taskID
            response = requests.delete(URL, headers=self.headers)

            # Need some error handling here
            if response.status_code!=200:
                return

            if i.task.task_type == "habit":
                G.HabitMenu.Remove(i.task.taskID)
            elif i.task.task_type == "daily":
                G.DailyMenu.Remove(i.task.taskID)
            elif i.task.task_type == "todo":
                G.TODOMenu.Remove(i.task.taskID)

        #
        #
        #
        #for i in self.EditQueue:
        #TODO: Needs to be updated to V3 API
        if(False):
            URL = GET_TASKS_URL + "/" + i.task.taskID
            response = requests.put(URL, headers=self.headers, json=i.task.data)

            # Need some error handling here
            if response.status_code!=200:
                return

        #
        #
        # Update the Interface
        G.screen.Erase()
        G.user.PrintDiff(diffDict)
        G.intf.Init()
        G.user.PrintUserStats()

        #
        #
        #
        # Display Drop Messages
        if Drops:
            G.screen.SaveInRegister(1)
            drop_items = []
            for i in Drops:
                DEBUG.Display("Processing Drop %s..." % i);
                drop_items += [M.SimpleTextItem(i)]

            dropMenu = M.SimpleTextMenu(drop_items, C.SCR_TEXT_AREA_LENGTH)
            dropMenu.SetXY(C.SCR_FIRST_HALF_LENGTH, 5)
            dropMenu.Display()
            dropMenu.Input()
            G.screen.RestoreRegister(1)

        self.ClearQueues()


    #Add a new task
    def CreateTask(self, title, task_type):

        #TODO: Needs to be updated to V3 API
        return 0

	task = {}
	task['text'] = title.decode("utf-8")
	task['type'] = task_type
	task['priority'] = 1

	if task_type == 'todo' or task_type == 'daily':
	    task['checklist'] = []
	if task_type == "daily":
	    task['everyX'] = 1
	    task['frequency'] = 'weekly'
	    task['repeat'] = {'m': True, 't': True, 'w': True, 'th': True, 'f': True, 's': True, 'su': True}
	if task_type == "habit":
	    task['up'] = True
	    task['down'] = True


	DEBUG.Display("Creating Task...");
	response = requests.post(GET_TASKS_URL, headers=self.headers, json=task)

	# Need some error handling here
	if response.status_code!=200:
	    DEBUG.Display("Failed")
	    return

	DEBUG.Display(" ")
	ret_task = response.json()
	if task_type == "habit":
            item = T.Habit(ret_task)
            menu_item = M.MenuItem(item, "habit", item.text)
	    G.HabitMenu.Insert(menu_item)

        elif task_type == "daily":
            item = T.Daily(ret_task)
            menu_item = M.MenuItem(item, "daily", item.text)
	    G.DailyMenu.Insert(menu_item)

	elif task_type == "todo":
            item = T.TODO(ret_task)
            menu_item = M.MenuItem(item, "todo", item.text)
	    G.TODOMenu.Insert(menu_item)





