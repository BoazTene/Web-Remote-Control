import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from .GET.GET import GET
from .POST.POST import POST


class Handler(BaseHTTPRequestHandler):
    """"""

    def __init__(self, *args, directory=None, **kwargs):
        if not mimetypes.inited:
            mimetypes.init()  # try to read system mime.types

        self.root_directory = "../HTTP_Server/wasm/site/Main"

        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handles the GET requests"""
        GET(self, self.path, self.root_directory)

    def do_POST(self):
        POST(self)

    def log_message(self, format, *args):
        pass

