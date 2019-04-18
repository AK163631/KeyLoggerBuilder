from abc import ABC, abstractmethod


class PluginBase(ABC):

    @abstractmethod
    def write(self, buffer: dict):
        pass


