import random, socket


# This function generates a random port to a connection and checks if the port is in use or not
# at the end the port will be saved at the self.port
class GetPort:
    def __init__(self):
        self.START_PORT = 0
        self.END_PORT = 0

        self.port = self.random_port()

        while not self.check_port():
            self.port = self.random_port()

    # checking if the port is in use
    def check_port(self):
        ADDRESS = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if s.connect_ex((ADDRESS, self.port)) == 0:
            return True
        else:
            return False

    # generates a random port to use
    def random_port(self):
        return random.randint(self.START_PORT, self.END_PORT)