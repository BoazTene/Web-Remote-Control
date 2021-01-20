import socket
from RemoteMachine.HandShake.util import *


class UdpHandShake:
    """
    This class is the Udp handshake.

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

    def __init__(self, creds, host):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.port = int(creds[1][0])
            self.key = creds[1][1]
        except ValueError:
            self.port = int(creds[1][1])
            self.key = creds[1][2]

        self.host = host
        self.success = False

        self.send_key()

        if self.OK("ok"):
            if self.OK("ok"):
                self.get_client()
                self.session.sendto(b"Ok, Client", self.addr)
                print("The HandShake completed successfully")
                self.success = True
                return
            else:
                print("The HandShake failed because of the remote client.")
                return
        else:
            print("The key isn't correct.")

    def get_client(self):
        """
        This function is used to perform the fifth stage at the handshake.
        The function will receive from the server the address of the other one.
        :return:
        """
        data, addr = self.session.recvfrom(1024)
        self.addr = msg_to_addr(data)

    def send_key(self):
        self.session.sendto(self.key.encode("utf-8"), (self.host, self.port))

    def OK(self, recv):
        """
        This function is used to confirm any ok messages from the server during the handshake.
        :param recv:
        :return:
        """

        try:
            data, addr = self.session.recvfrom(1024)
        except Exception:
            return False

        data = data.decode('utf-8')

        if data.lower() == recv:
            return True
        elif data == "Alive Check":
            return self.OK(recv)
        else:
            print("Failed! " + data)
            return False