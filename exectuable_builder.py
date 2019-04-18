import PyInstaller


class Builder:
    """
    store configs in configuration file
    embed config file with exe at build time

    build_spec = {encrypt_config="key_password",
                encrypt_log="key_password",
                plugin_name="**kwargs" or True if no **kwargs,
                plugin_config=""}

    config={
        plugin="plugin to use"
        write_interval= "weekly" or "daily" or "hourly" or "onPress" or "never"
        plugin_config="{config for plugin}"
    }
    """

    def __init__(self, **build_spec):
        pass
