from http.server import HTTPServer
from .Handler.Handler import Handler


def run(port=8080, server_class=HTTPServer, handler_class=Handler):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

