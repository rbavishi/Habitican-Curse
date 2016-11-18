""" Module "DEBUG" : Wrapper for displaying messages

"""

# Custom module imports
import screen as Screen
import global_objects as G
import config as C
import logging

logging.basicConfig(filename="habitican_curse.log",level=logging.WARN)

#Clear the curses display and send a new string
def Display(string):
    G.screen.Display(" "*(C.SCR_Y-1))
    G.screen.Display(string)
    if string is not " ":
        logging.debug("CURSES DISPLAY - %s" % string)

#Send a message to the logging facility
# This existis so we don't depend everything on the python
# logging module
def Log(level, string):
    logging.log(level, string)
