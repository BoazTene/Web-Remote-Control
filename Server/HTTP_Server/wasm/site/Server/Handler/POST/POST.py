from http import HTTPStatus


class POST:
    def __init__(self, handler):
        self.handler = handler

        self.send_error(HTTPStatus.FORBIDDEN, "Forbidden", explain="This site doesn't support POST requests.")
        self.end_headers()

    def send_error(self, code, message=None, explain=None):
        self.handler.send_error(code, message=message, explain=explain)

    def end_headers(self):
        self.handler.end_headers()