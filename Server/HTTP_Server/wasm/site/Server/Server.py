from http.server import HTTPServer
from Handler.Handler import Handler


def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run(port=5000)