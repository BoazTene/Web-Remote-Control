from HttpApi.HostHandler.CheckAlive import CheckAlive
# from HttpApi.HostHandler.Keyboard import keyboard
from HttpApi.HostHandler.Mouse import Mouse
from HttpApi.HostHandler.SendImage import SendImage


class HostHandler:
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
        self.session = session
        self.address = address

        self.check_alive = CheckAlive(self.session, self.address, self.ALIVE_CHECK_BREAKER)
        self.images = SendImage(self.session, self.address, self.IMAGE_BREAKER)

        self.check_alive.start()
        self.images.start()

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
        return {breaker for breaker in [breaker[0] for breaker in self.BREAKERS] if breaker in data}

    def keyboard(self, data):
        pass

    def mouse(self, data):
        pass

    def check_alive_recv(self):
        self.check_alive = True

    def run(self):
        """
        This function listens to incoming messages and acting by the messages
        """

        try:
            while self.check_alive.is_alive():
                data = self.get_data()
                start_breakers = self.find_start_breaker(data)

                for i in start_breakers:
                    if i == self.KEYBOARD_BREAKER:
                        self.keyboard(data)
                    elif i == self.MOUSE_BREAKER:
                        self.mouse(data)
                    elif i == self.ALIVE_CHECK_BREAKER:
                        self.check_alive_recv()
        except Exception:
            return
