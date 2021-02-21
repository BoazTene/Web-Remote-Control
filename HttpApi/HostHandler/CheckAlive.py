import socket
from eventlet.timeout import Timeout
# from HttpApi.HostHandler.Handler import HostHandler
from time import sleep
import time
import threading


class CheckAlive(threading.Thread):
    """
    This class sends every 10 seconds check alive message to the client to make sure he still connected.
    The client has 5 second to answer, after that he will considered as not connected.
    """

    TIMEOUT = 5
    DELAY = 10

    def __init__(self, session, address, alive_check_breaker):
        super().__init__()
        self.session = session
        self.address = address

        self.ALIVE_CHECK_BREAKER = alive_check_breaker

        self.timeout = None
        self.recv_ok = False

    def send_check_alive(self):
        """
        This function sends the check alive message
        """
        print("send")
        self.session.sendto(self.ALIVE_CHECK_BREAKER[0].encode("utf-8"), self.address)

    def start_timeout(self):
        """
        This function starts timeout
        :return:
        """

        return Timeout(self.TIMEOUT, TimeoutError)

    def stop_timeout(self):
        """
        This function stops the timeout
        :return:
        """

        self.timeout.cancel()

    def run(self):
        """
        This is the main handler for the check alive.
        :return:
        """

        while True:
            sleep(self.DELAY)
            start_time = time.time()

            self.send_check_alive()
            while time.time() - start_time < self.TIMEOUT:
                if self.recv_ok:
                    print("recv")
                    self.recv_ok = False
                    # self.stop_timeout()
                    break
            if self.recv_ok:
                continue
            else:
                return





