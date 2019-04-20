import datetime
from abc import ABC, abstractmethod


class PluginBase(ABC):

    @abstractmethod
    def write(self, date_time: datetime.datetime, window: str, key: str):
        pass


