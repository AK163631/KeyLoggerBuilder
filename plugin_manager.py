import importlib
import inspect
import json

from plugins.plugin_base import PluginBase


class PluginManager:
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

    def __init__(self):
        """
        if self._CONFIG_AES_PASSWORD:
            config = self.decrypt_config()
        else:
            config = json.load(open(self._CONFIG_FILE, "r"))
        """

        config = {"plugin_name": "http_server", "class_name": "HttpServer", "plugin_config": {}}

        class_members = inspect.getmembers(
            importlib.import_module("plugins." + config["plugin_name"]), inspect.isclass)

        if "class_name" in config.keys():
            for name, class_ in class_members:
                if name == config["class_name"]:
                    plugin_class = class_
                    break
            else:
                raise Exception(f"plugin not found {config['class_name']} in {config['plugin_name']}")
        else:
            plugin_class = class_members[0][1]  # assume class will be first found in module

        self.__plugin = plugin_class(**config["plugin_config"])  # type: PluginBase

        if not issubclass(self.plugin.__class__, PluginBase):  # check if plugin is subclass of PluginBase
            raise Exception(f"{self.plugin.__class__} is not sub class of PluginBase")

    def decrypt_config(self) -> dict:
        from plugins.utils.crypto import Crypto
        crypto = Crypto(self._CONFIG_AES_PASSWORD)
        return json.loads(crypto.decrypt(open(self._CONFIG_FILE, "rb").read()))

    @property
    def plugin(self) -> PluginBase:
        return self.__plugin

# PluginManager()
