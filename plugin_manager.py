import functools
import importlib
import inspect
import json
import time
import schedule
from threading import RLock
from threading import Thread

from plugins.plugin_base import PluginBase


def thread_lock(func):
    """
    acquires lock, executes function then releases lock
    """

    @functools.wraps(func)
    def stub(self, *args, **kwargs):
        self.lock.acquire()
        ret = func(self, *args, *kwargs)
        self.lock.release()
        return ret

    return stub


class PluginManager(Thread):
    """
    Loads and unloads plugins based on embed config file
    contains a handful of functions based ono the interval to wait
    between sending the buffer.

    config={
        plugin="plugin module name to use"
        write_interval= "daily" or "hourly" or "on_press" or "never"
        plugin_config="{config for plugin}"
    }
    """
    _CONFIG_FILE: str = "config.json"
    _CONFIG_AES_PASSWORD: str = ""  # OVER WRITTEN

    def __init__(self, buffer: dict, lock: RLock):
        super().__init__()
        #  maps interval options to function
        self.__function_mapping = {"daily": self.__daily, "hourly": self.__hourly,
                                   "on_press": self.__on_press, "never": self.__never()}
        self.lock = lock
        self.buffer = buffer  # dependency injected reference to buffer
        if self._CONFIG_AES_PASSWORD:
            # decrypt config file here
            config = dict()
        else:
            config = json.load(self._CONFIG_FILE)

        self.scheduler = self.__function_mapping[config["write_interval"]]
        plugin = inspect.getmembers(
            importlib.import_module(config["plugin"], package="plugins"), inspect.isclass)[0][1]
        self.plugin = plugin(**config["plugin_config"])  # type: PluginBase

        if not issubclass(self.plugin.__class__, PluginBase):  # check if plugin is subclass of PluginBase
            raise Exception(f"{self.plugin.__class__} is not sub class of PluginBase")

    def run(self):
        """
        Run selected scheduler function for ever
        """
        while True:
            self.scheduler()

    @thread_lock
    def __clear_buffer(self):
        """
        Clears buffer dictionary
        """
        self.buffer.clear()

    def __task(self):
        """
        Write buffer to plugin then clear the buffer
        """
        self.plugin.write(self.buffer)
        self.__clear_buffer()

    def __daily(self):
        """
        Run __task daily at 12:00
        """
        schedule.every().day.at("12:00").do(self.__task)

    def __hourly(self):
        """
        Run __task hourly
        """
        schedule.every().hour.do(self.__task)

    def __on_press(self):
        """
        Run __task every time the buffer is updated
        """
        buff = dict(self.buffer)
        while buff == self.buffer:
            time.sleep(1)  # wait until buffer has changed
        else:
            self.__task()

    def __never(self):
        """
        Wait sleep for an hour for ever.
        Don't see this function ever getting used here for completeness
        """
        time.sleep(3600)
