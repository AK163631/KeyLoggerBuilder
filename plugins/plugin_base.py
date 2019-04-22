import datetime
from abc import ABC, abstractmethod


class PluginBase(ABC):

    @abstractmethod
    def write(self, date_time: datetime.datetime, window: str, key: str):
        pass

    def close(self):
        pass

    def __del__(self):
        self.close()


