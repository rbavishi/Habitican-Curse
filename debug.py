""" Module "DEBUG" : Wrapper for displaying messages

"""

# Custom module imports
import screen as Screen
import global_objects as G
import config as C


def Display(string):
    G.screen.Display(" "*C.SCR_X)
    G.screen.Display(string)
