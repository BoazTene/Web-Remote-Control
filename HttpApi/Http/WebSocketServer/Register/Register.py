from HttpApi.HostHandler.Main import Main


class Register:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def register(self):
        handler = Main(self.ip, self.port, self.username, self.password)
        handler.start()

        return handler


