""" Module "Content" : Manage Habitica Content

    All info related to quests, items etc. i.e. the basic Habitica Content
    is stored here. All fetching takes constant time.
"""

# Standard Library Imports
import requests
import time

# Custom Module Imports

import config as C
from screen import Screen
import global_objects as G
import helper as H
import menu as M
import task as T
import debug as DEBUG
import user as U

FETCH_URL = "https://habitica.com:443/api/v2/content"

class ContentManager(object):
    """ Class for managing Habitica content """

    def __init__(self):
	#DEBUG.Display("Content Fetching in progress...")
	resp = self.Fetch()
	if resp.status_code == 200:
	    self.contentDict = resp.json()
	else:
	    self.contentDict = -1

    def Fetch(self):
	resp = requests.get(FETCH_URL)
	return resp

    def Quest(self, key):
	return self.contentDict['quests'].get(key, {})


class Party(object):
    """ Class for storing party info, displaying chat menus, 
    	quest details(if any) etc. """

    def __init__(self, party):
	self.party = party

	# Some Basic Details
	self.name    = str(party['name'])
	self.members = [str(i['profile']['name']) for i in party['members']]
	self.chat    = party['chat']
	chat_items = []
	chatList = self.chat[:50]
	for i in chatList:
	    timeElapsed = H.GetDifferenceTime(i['timestamp'])
	    detailString = i.get('user', '') + " " + timeElapsed
	    chat_items += [M.SimpleTextItem(str(i['text']), additional=str(detailString))]

	self.chatMenu = M.SimpleTextMenu(chat_items, C.SCR_TEXT_AREA_LENGTH)

	self.quest = party.get('quest', None)
	if self.quest != None:
	    while (G.content == None):
		DEBUG.Display("Fetching Content...")
		time.sleep(5)
	    DEBUG.Display(" ")

	    self.questDetails = G.content.Quest(str(self.quest['key']))
	    self.questText    = str(self.questDetails['text'])

	    self.questType = ""

	    if self.questDetails.has_key('boss'):
		self.questType     = "boss"
		self.bossMaxHealth = self.questDetails['boss']['hp']
		self.bossName      = self.questDetails['boss']['name']
		self.bossRage      = self.questDetails['boss'].get('rage', None)
		self.bossStrength  = self.questDetails['boss']['str']

		self.progress      = int(round(party['quest']['progress']['hp'],0))

	    elif self.questDetails.has_key('collect'):
		self.questType     = "collect"
		self.questItems    = self.questDetails['collect']
		self.progress      = party['quest']['progress']['collect']


    def Display(self):
	G.screen.ClearTextArea()
	X, Y = C.SCR_FIRST_HALF_LENGTH-2, 1
	MAX_X = C.SCR_X - 3

	titleString = "".join([self.name, " : "]+[i+", " for i in self.members[:-1]]+[self.members[-1]])
	G.screen.DisplayCustomColorBold(titleString, C.SCR_COLOR_MAGENTA, X, Y)
	G.screen.DisplayCustomColor("-"*(C.SCR_Y-2), C.SCR_COLOR_LIGHT_GRAY, X+1, Y)
	X += 2

	if self.quest != None:
	    G.screen.DisplayBold("Quest: "+self.questText, X, Y)
	    X += 1
	    if self.questType == "boss":
		# Display Boss Stats
		G.screen.DisplayCustomColorBold(str(self.bossName)+" "+C.SYMBOL_HEART+" : "+
					 str(self.progress)+"/"+str(self.bossMaxHealth), 
					 C.SCR_COLOR_RED, MAX_X, Y)

		MAX_X -= 1

	self.chatMenu.SetXY(X+1, 1) 
	self.chatMenu.SetNumRows(MAX_X - (X + 1))
	self.chatMenu.Display()
	self.chatMenu.Input()



