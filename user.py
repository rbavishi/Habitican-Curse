""" Module "User" : User stats and profile

    All user related data such as health, gold, mana etc. are stored here
"""

# Custom Module Imports

import config as C
import global_objects as G
import debug as DEBUG
import request_manager as RM
import helper as H
import menu as M


def Round(num):
    return int(round(num, 0))


# Display positive numbers as +N and negative numbers as -N 
def SignFormat(num):
    if num == 0:
        return ""

    return '{0:+d}'.format(num)


class User(object):
    """ Class to store user data """

    def __init__(self, data):
 
        self.data = data

        # Basic User Stats
        self.hp          = Round(data['hp'])
        self.maxHealth   = Round(data['maxHealth'])
        self.mp          = Round(data['mp'])
        self.maxMP       = Round(data['maxMP'])
        self.gp          = Round(data['gp'])
        self.exp         = Round(data['exp'])
        self.toNextLevel = Round(data['toNextLevel'])
        self.lvl         = data['lvl']

        self.cursorPositions = []

    # Written separately to avoid confusion
    def Reload(self, data):

        # Basic User Stats
        self.hp          = Round(data['hp'])
        self.maxHealth   = Round(data['maxHealth'])
        self.mp          = Round(data['mp'])
        self.maxMP       = Round(data['maxMP'])
        self.gp          = Round(data['gp'])
        self.exp         = Round(data['exp'])
        self.toNextLevel = Round(data['toNextLevel'])
        self.lvl         = data['lvl']

    def PrintData(self):
        G.screen.DisplayCustomColor(" "*(C.SCR_Y-1), C.SCR_COLOR_WHITE_GRAY_BGRD, C.SCR_X-2, 0)

        cursor = 1
        self.cursorPositions = []

        # Level
        string = C.SYMBOL_LEVEL + " " + str(self.lvl)
        G.screen.DisplayCustomColorBold(string, C.SCR_COLOR_WHITE_GRAY_BGRD, C.SCR_X-2, cursor)

        self.cursorPositions.append(cursor)
        cursor += len(string) + 3 - len(C.SYMBOL_LEVEL)

        # Health
        string = C.SYMBOL_HEART + " " + str(self.hp)+"/"+str(self.maxHealth)
        G.screen.DisplayCustomColorBold(string, C.SCR_COLOR_RED_GRAY_BGRD, C.SCR_X-2, cursor)

        self.cursorPositions.append(cursor)
        cursor += len(string) + 3 - len(C.SYMBOL_HEART)

        # XP
        string = C.SYMBOL_EXPERIENCE + " " + str(self.exp)+"/"+str(self.toNextLevel)
        G.screen.DisplayCustomColorBold(string, C.SCR_COLOR_GREEN_GRAY_BGRD, C.SCR_X-2, cursor)

        self.cursorPositions.append(cursor)
        cursor += len(string) + 3 - len(C.SYMBOL_EXPERIENCE)

        # Mana
        string = C.SYMBOL_MANA + " " + str(self.mp)+"/"+str(self.maxMP)
        G.screen.DisplayCustomColorBold(string, C.SCR_COLOR_BLUE_GRAY_BGRD, C.SCR_X-2, cursor)

        self.cursorPositions.append(cursor)
        cursor += len(string) + 3 - len(C.SYMBOL_MANA)

        # Gold
        string = C.SYMBOL_GOLD + " " + str(self.gp)
        G.screen.DisplayCustomColorBold(string, C.SCR_COLOR_YELLOW_GRAY_BGRD, C.SCR_X-2, cursor)

        self.cursorPositions.append(cursor)
        cursor += len(string) + 3 - len(C.SYMBOL_GOLD)

    def PrintDiff(self, diffDict):
        for i in diffDict:
            diffDict[i] = Round(diffDict[i])
            self.data[i] = self.data[i] + diffDict[i]
            diffDict[i] = SignFormat(diffDict[i])

        self.Reload(self.data)

        # Difficult to maintain the correct increase in experience when level changes
        if diffDict['lvl'] != "":
            diffDict['exp'] = ""

        # Level
        G.screen.DisplayCustomColorBold(diffDict['lvl'], C.SCR_COLOR_WHITE, C.SCR_X-3, self.cursorPositions[0]+2)
                     
        # Health
        G.screen.DisplayCustomColorBold(diffDict['hp'], C.SCR_COLOR_RED, C.SCR_X-3, self.cursorPositions[1]+2)

        # Experience
        G.screen.DisplayCustomColorBold(diffDict['exp'], C.SCR_COLOR_GREEN, C.SCR_X-3, self.cursorPositions[2]+2)
                     
        # Mana
        G.screen.DisplayCustomColorBold(diffDict['mp'], C.SCR_COLOR_BLUE, C.SCR_X-3, self.cursorPositions[3]+2)
                     
        # Gold
        G.screen.DisplayCustomColorBold(diffDict['gp'], C.SCR_COLOR_YELLOW, C.SCR_X-3, self.cursorPositions[4]+2)

    def GetPartyData(self):
        resp = G.reqManager.PartyRequest()

        # Need some error handling here
        if resp.status_code != 200:
            return 

        data = resp.json()
        chat_items = []
        chat = data['chat'][:50]
        for i in chat:
            timeElapsed = H.GetDifferenceTime(i['timestamp'])
            detailString = i.get('user', '') + " " + timeElapsed
            chat_items += [M.SimpleTextItem(str(i['text']), additional=str(detailString))]

        chatMenu = M.SimpleTextMenu(chat_items, C.SCR_X-(C.SCR_MAX_MENU_ROWS+7+4))
        chatMenu.SetXY(C.SCR_MAX_MENU_ROWS+7, 5) 
        chatMenu.Display()
        chatMenu.Input()



