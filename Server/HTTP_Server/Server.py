from http.server import HTTPServer
from .Handler.Handler import Handler


def run(port=8080, host="0.0.0.0", server_class=HTTPServer, handler_class=Handler):
    """
    This function starts the web server.

    :param host:
    :param port:
    :param server_class:
    :param handler_class:
    :return:
    """

    server_address = (host, port)
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

