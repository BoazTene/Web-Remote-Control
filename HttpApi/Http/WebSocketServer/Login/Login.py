from HttpApi.ClientHandler.Main import Main


class Login:
    PORT = 8080

    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def login(self):
        handler = Main(self.ip, self.PORT, self.username, self.password)

        result = handler.run()

        return handler.image_handler, handler.keyboard_handler, result
