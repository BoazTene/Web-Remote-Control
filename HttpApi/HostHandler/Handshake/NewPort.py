import socket


class NewPort:
    """
    This class is used to open new udp hole punching ports.
    To use this class the client and host must have at least one hole punching port.

    The stages:
        1. client create new socket object in order to get new nat port.
        2. The client sends an hello message to the old port from the new nat port
        3. The host answers him from a new part to the new nat port

    Now the client and the host opened new port to talk.
    """

    def __init__(self, s, address):
        self.old_s = s
        self.address = address

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("", 0))

    def send_massage(self, address):
        """
        This function is used to send the hello message to the client from the new nat port
        :return:
        """

        self.s.sendto(b"Hello", address)

    def get_client(self):
        """
        This function receives from the client the his new nat address
        :return:
        """

        ip, port = self.s.recvfrom(1024)[1]
        return ip, int(port)

    def run(self):
        """
        This is the main handler.
        :return:
        """

        self.send_massage(self.address)

        address = self.get_client()

        for i in range(10):
            self.send_massage(address)

        return self.s, address
