import socket


class UDPHandshake:
    """
    This class is the Udp handshake for the host.

    The udp handshake is a upgrade to the tcp connection,
    to perform it the tcp handshake but be already made.

    handshake stages:
    1. The server will send a string 'port!key' in the tcp connection.
    2. The client will send a packet to the server in the port, in the packet's data will be the key.
    3. The server will replay with an yes or no. yes means key is correct and no means wrong.
    4. The server will send an yes or no. yes means the HandShake went successfully and no means that the other machine failed.
    5. The server will exchange the address between the two machines.
    6. Each client will send to the other one an ok message.

    The udp hole punching successfully done.
    """

    def __init__(self, tcp_session, host):
        self.tcp_session = tcp_session

        port, self.key = self.get_port_and_key()

        self.address = (host, port)

        self.session = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_port_and_key(self):
        """
        This function is the first stage in the handshake
        This function return the port and key from the server.

        :return:
        """

        while True:
            data = self.tcp_session.recv(1024).decode("utf-8")
            if data != "Alive Check":
                break

        return int(data.split("!")[0]), data.split("!")[1]

    def send_creds(self):
        """
        This function is the second stage in the handshake.
        This function sends to the server the username and password.

        :return:
        """

        self.session.sendto(self.key.encode("utf-8"), self.address)

    def ok_message(self, recv):
        """
        This function returns if the server sends an ok message or not.
        :param recv:
        :return:
        """

        return True if self.session.recvfrom(1024)[0].decode("utf-8").lower() == recv.lower() else False

    def msg_to_addr(self, data):
        """
        This function returns the ip, port of the second client from a string.
        """

        ip, port = data.decode('utf-8').strip().split(':')
        return ip, int(port)

    def get_client(self):
        """
        This function is the fifth stage in the handshake.
        This function will recv from the server the second client address.
        :return:
        """

        data, addr = self.session.recvfrom(1024)
        if data == b'Ok, Client':
            data, addr = self.session.recvfrom(1024)
            self.address = self.msg_to_addr(data)
            return True
        else:
            self.address = self.msg_to_addr(data)
            return False

    def run(self):
        """
        This function is the main handler for the handshake.
        :return:
        """

        self.send_creds()
        if self.ok_message('ok'):
            if self.ok_message('ok'):
                if self.get_client() or self.ok_message('ok, client'):
                    print("The HandShake completed successfully")
                    return True
                else:
                    print("Something bad happened..")
                    return False
            else:
                print("The HandShake failed because of the remote client.")
                return False
        else:
            print("The key isn't correct.")
            return False
