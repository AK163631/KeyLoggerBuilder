import datetime
import atexit
from abc import ABC, abstractmethod


class PluginBase(ABC):
    """
    Base class for all plugins, a plugin will not be registered unless it
    subclasses PluginBase, data is passed between daemon and plugin via self.write
    """

    @abstractmethod
    def write(self, date_time: datetime.datetime, window: str, key: str):
        """
        Write key press and relevant data to target plugin

        :param date_time: Date and time when key was pressed
        :param window: Window key was pressed in
        :param key: Key press character
        """
        pass

    def close(self):
        """
        close handler
        """
        pass

    def register_exit_handler(self):
        """
        register self.close function at exit
        """
        atexit.register(self.close)


