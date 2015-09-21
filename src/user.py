""" Module "User" : User stats and profile

    All user related data such as health, gold, mana etc. are stored here
"""

# Custom Module Imports

import config as C
import global_objects as G
import debug as DEBUG
import request_manager as RM


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

        if diffDict['lvl'] != "":
            diffDict['exp'] = ""

        # Level
        G.screen.DisplayCustomColorBold(diffDict['lvl'], C.SCR_COLOR_WHITE, C.SCR_X-3, self.cursorPositions[0])
                     
        # Health
        G.screen.DisplayCustomColorBold(diffDict['hp'], C.SCR_COLOR_RED, C.SCR_X-3, self.cursorPositions[1])

        # Experience
        G.screen.DisplayCustomColorBold(diffDict['exp'], C.SCR_COLOR_GREEN, C.SCR_X-3, self.cursorPositions[2])
                     
        # Mana
        G.screen.DisplayCustomColorBold(diffDict['mp'], C.SCR_COLOR_BLUE, C.SCR_X-3, self.cursorPositions[3])
                     
        # Gold
        G.screen.DisplayCustomColorBold(diffDict['gp'], C.SCR_COLOR_YELLOW, C.SCR_X-3, self.cursorPositions[4])
