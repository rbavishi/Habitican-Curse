""" Module "Screen" : Wrapper for the ncurses screen

    All screen related functions such as displaying text, colors, background,
    saving/restoring context etc. go here.
"""
# Standard Library Imports
import curses
import tempfile

# Custom Module Imports

# from import * is bad practice, but we use it just for convenience in case of
# constants
from config import *


class Screen:

    def __init__(self, screen):
        self.screen = screen

        # These are special context registers.
        # Use these to store some important backtrack points.
        self.ctxts = []
        for i in xrange(NUM_CONTEXT_REGISTERS):
            self.ctxts += [tempfile.TemporaryFile()]

        self.active_registers = [False]*NUM_CONTEXT_REGISTERS

        # This is the stack for saving contexts.
        # Use these to get a proper order of backtrack points
        self.stackFile = tempfile.TemporaryFile()
        self.stack = []

    def Initialize(self):
        # Cursor not visible
        curses.curs_set(0)

        # Color and Background
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(SCR_COLOR_RED, curses.COLOR_RED, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_GREEN, curses.COLOR_GREEN, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_YELLOW, curses.COLOR_YELLOW, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_MAGENTA, curses.COLOR_MAGENTA, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_BLUE, curses.COLOR_BLUE, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_WHITE, curses.COLOR_WHITE, SCR_COLOR_BGRD)

        curses.init_pair(SCR_COLOR_LIGHT_ORANGE, 209, SCR_COLOR_BGRD)
        curses.init_pair(SCR_COLOR_DARK_ORANGE, 208, SCR_COLOR_BGRD)

        curses.init_pair(SCR_COLOR_BLUE_GRAY_BGRD, 19, 244)
        curses.init_pair(SCR_COLOR_GRAY_BLUE_BGRD, 244, 19)

        # Same as writing " " in white on a black background
        self.screen.bkgd(' ', curses.color_pair(SCR_COLOR_WHITE))

    def Refresh(self):
        self.screen.refresh()

    def Erase(self):
        self.screen.erase()

    def Clear(self):
        self.screen.clear()

    def SaveInRegister(self, register):
        # Should be between 0 and NUM_CONTEXT_REGISTERS-1
        if register >= NUM_CONTEXT_REGISTERS:
            return

        self.ctxts[register].seek(0)
        self.screen.putwin(self.ctxts[register])
        self.active_registers[register] = True

    def RestoreRegister(self, register):
        # Should be between 0 and NUM_CONTEXT_REGISTERS-1
        if register >= NUM_CONTEXT_REGISTERS:
            return

        # Register is empty
        if not self.active_registers[register]:
            return

        self.screen = curses.getwin(self.ctxts[register])
        self.Refresh()

    def Save(self):
        self.stack.append(self.stackFile.tell())
        self.screen.putwin(self.stackFile)

    def Restore(self):
        # Stack cannot be empty
        if len(self.stack) == 0:
            return

        self.stackFile.seek(self.stack[-1])
        self.screen = curses.getwin(self.stackFile)
        self.Refresh()

    def Display(self, string, x=0, y=0):
        self.screen.addstr(x, y, string)
        self.Refresh()

    def DisplayBold(self, string, x=0, y=0):
        self.screen.addstr(x, y, string, curses.A_BOLD)
        self.Refresh()

    def Highlight(self, string, x=0, y=0):
        self.screen.addstr(x, y, string, curses.A_BOLD |
                                         curses.color_pair(SCR_COLOR_BLUE_GRAY_BGRD))
        self.Refresh()

    def DisplayCustomColor(self, string, color=0, x=0, y=0):
        self.screen.addstr(x, y, string, curses.color_pair(color))
        self.Refresh()

    def DisplayCustomColorBold(self, string, color=0, x=0, y=0):
        self.screen.addstr(x, y, string, curses.A_BOLD |
                                         curses.color_pair(color))
        self.Refresh()
