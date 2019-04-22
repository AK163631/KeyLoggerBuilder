from plugins.plugin_base import PluginBase
import smtplib

from plugins.utils.time_delta import TimeDelta


class Email(PluginBase):

    def __init__(self, email=None, interval="on_press"):
        if email is None:
            raise IOError("No email specified")

        self.email = email
        self.interval = TimeDelta().map[interval]

    def write(self, date_time, window, key):
        pass
