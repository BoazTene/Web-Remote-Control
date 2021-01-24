from HttpApi.HostHandler.CheckAlive import CheckAlive
from HttpApi.HostHandler.Keyboard import Keyboard
from HttpApi.HostHandler.Mouse import Mouse
from HttpApi.HostHandler.SendImage import SendImage
import threading


class HostHandler(threading.Thread):
    """
    This class is the http api for the host.
    """

    MAX_IMAGE_DGRAM = 2 ** 16 - 64
    IMAGE_BREAKER = ["<start>", "<end>"]
    ALIVE_CHECK_BREAKER = ["<check-alive>"]
    KEYBOARD_BREAKER = ["<key-s>", "<key-e>"]
    MOUSE_BREAKER = ["<mouse-s>", "<mouse-e>"]
    BREAKERS = [IMAGE_BREAKER, ALIVE_CHECK_BREAKER, KEYBOARD_BREAKER, MOUSE_BREAKER]

    def __init__(self, session, address):
        super().__init__()
        self.session = session
        self.address = address

        self.images = SendImage(self.session, self.address, self.IMAGE_BREAKER)
        self.check_alive = CheckAlive(self.session, self.address, self.ALIVE_CHECK_BREAKER)

        self.check_alive.start()
        self.images.start()
        print("STart")

    def get_data(self):
        """
        This function recv the max amount of bytes from the host
        """
        return self.session.recvfrom(self.MAX_IMAGE_DGRAM)

    def find_start_breaker(self, data):
        """
        :data: str

        This function returns all the start breakers in data
        """
        start_breakers = [breaker[0] for breaker in self.BREAKERS]
        return [breaker for breaker in start_breakers if breaker in data]

    def mouse(self, data):
        Mouse(self.session, self.address, data, self.MOUSE_BREAKER).set_pos()

    def check_alive_recv(self):
        """
        This function is used to tell the check alive class that the client received to the ok message.
        :return:
        """

        self.check_alive.recv_ok = True

    def run(self):
        """
        This function listens to incoming messages and acting by the messages
        """

        while True:
            data = self.get_data()
            start_breakers = self.find_start_breaker(data[0].decode("utf-8"))
            for i in start_breakers:
                if i == self.MOUSE_BREAKER[0]:
                    self.mouse(data[0].decode("utf-8"))
                elif i == self.ALIVE_CHECK_BREAKER[0]:
                    self.check_alive_recv()

