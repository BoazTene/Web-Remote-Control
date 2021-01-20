import random, socket


class GetPort:
    """
    This function generates a random port to a connection and checks if the port is in use or not
    at the end the port will be saved at the self.port
    """

    START_PORT = 300
    END_PORT = 10000

    def __init__(self):
        self.port = self.random_port()

        while not self.check_port():
            self.port = self.random_port()

    def check_port(self):
        """
        checking if the port is in use
        :return:
        """

        ADDRESS = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if s.connect_ex((ADDRESS, self.port)) == 0:
            return False
        else:
            return True

    def random_port(self):
        """
        generates a random port to use
        :return:
        """
        return random.randint(self.START_PORT, self.END_PORT)
