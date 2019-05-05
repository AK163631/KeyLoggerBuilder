from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from multiprocessing import Process

from plugins.plugin_base import PluginBase
from plugins.local_file import LocalFile


class HttpServer(PluginBase):
    """
    Plugin runs a http server in a daemon process.
    All logs a written to local_file which is then read by
    the http server and returned on each GET requests.
    """

    def __init__(self, ip: str = "127.0.0.1", port: int = 80):
        self.ip = ip
        self.port = port
        self.__local_file = LocalFile()
        self.__local_file.register_exit_handler()  # will delete log file when python exits
        self.__dispatch_process()  # dispatch http server daemon

    def write(self, *args):
        self.__local_file.write(*args)

    def __dispatch_process(self):
        """
        Start http server as a daemon process, will terminate if parent is terminated
        """
        p = Process(target=self.process_stub, args=(self.__local_file.path, self.ip, self.port))
        p.daemon = True
        p.start()

    @staticmethod
    def process_stub(path, ip, port):
        handler = partial(_Server, path)
        server = HTTPServer((ip, port), handler)
        server.serve_forever()


class _Server(BaseHTTPRequestHandler):
    """
    basic http server
    """

    def __init__(self, path: str, *args, **kwargs):
        self.file_path = path
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header(b'Content-type', b'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        try:
            self.wfile.write(open(self.file_path, "r").read().encode())
        except Exception as e:
            self.wfile.write(b'{"exception": ' + str(e).encode() + b'}')

    def do_HEAD(self):
        self._set_headers()
