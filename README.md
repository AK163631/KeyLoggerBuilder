# KeyLoggerBuilder
Plugable, Buildable Advanced Keylogger (.py -> .exe)

A keylogger is a program that collects and stores all key presses.  
This keylogger provides cross platform basic logging functionalities as well as advanced log exfiltration features and utilities.

# Log Exfiltration:
Currently there are 4 exfiltration modules however custom exfiltration modules are supported (more details below)
## emails
Sends an email of the captured logs based on a specified interval to a specified address. Once logs have been sent the local buffer is cleared.  
## http_post
Posts (http POST) logs to a specified URL, with the log buffer as the data attribute, based on a specified interval. Local logs are cleared after each request.
## http_server
Sets up a http server as a daemon process on a specified or default IP address and port, the logs are stored locally and are to be retrieved via a request to the server. 
## local_file
Writes log buffer to a specified or default local file.
# Utilities:
Helper functions and classes which can be used by exfilration modules
## time_delta
Provides functions that help to know when a time interval has passed
## crypto
Provides AES encryption and decryption functionalities
# Custom Plugins
One of the main features of the project is the support for custom exfiltration. Just ensure you class subclasses PluginBase in plugin_base.py and include the module and class name in the launch/build config and your good to go.
# Build
Support for easy buildablity (.py -> .exe) is partially implemented and will be completed shortly
