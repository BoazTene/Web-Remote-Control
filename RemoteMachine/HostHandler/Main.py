from RemoteMachine.HostHandler.Handshake import TCPHandshake, UDPHandshake
from RemoteMachine.HostHandler.Handler import HostHandler
import threading
import socket


class Main(threading.Thread):
    """
    This class is the main handler for the host.
    """

    def __init__(self, host_ip, port, username, password):
        super(Main, self).__init__()

        self.host_ip = host_ip
        self.port = port
        self.username = username
        self.password = password

        self.tcp_session = None
        self.udp_session = None
        self.udp_address = None

    def tcp_handshake(self):
        """
        This class handles the tcp Handshake
        :return:
        """

        tcp = TCPHandshake.TCPHandshake(self.host_ip, self.port, self.username, self.password)
        result = tcp.run()
        self.tcp_session = tcp.session

        return result

    def udp_handshake(self):
        """
        This function handles the udp handshake
        :return:
        """

        udp = UDPHandshake.UDPHandshake(self.tcp_session, self.host_ip)
        result = udp.run()

        self.udp_session = udp.session
        self.udp_address = udp.address

        return result

    def keep_alive(self, until_data):
        """
        This function wats until the server sends the until data value.
        :param until_data:
        :return:
        """

        while True:
            data = self.tcp_session.recv(1024).decode("utf-8")
            
            if data == until_data:
                self.tcp_session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                return

    def remote_control(self):
        """
        This function handles the remote control stage.
        :return:
        """

        handler = HostHandler(self.udp_session, self.udp_address)
        handler.run()

    def run(self):
        """
        The main function
        :return:
        """

        while self.tcp_handshake():
            self.keep_alive("Start-Remote-Control")

            if not self.udp_handshake():
                continue

            self.remote_control()
