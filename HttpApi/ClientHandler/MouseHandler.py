from HttpApi.HostHandler.CheckAlive import CheckAlive
from HttpApi.ClientHandler.Mouse import Mouse
import threading


class MouseHandler(threading.Thread):

    IMAGE_BREAKER = ["<start>", "<end>"]
    ALIVE_CHECK_BREAKER = ["<check-alive>"]
    KEYBOARD_BREAKER = ["<key-s>", "<key-e>"]
    MOUSE_BREAKER = ["<mouse-s>", "<mouse-e>"]
    BREAKERS = [IMAGE_BREAKER, ALIVE_CHECK_BREAKER, KEYBOARD_BREAKER, MOUSE_BREAKER]

    def __init__(self, session, address):
        super().__init__()
        self.session = session
        self.address = address

        self.check_alive = CheckAlive(self.session, self.address, self.ALIVE_CHECK_BREAKER)
        self.check_alive.start()

    def mouse(self, x, y, click, scroll):
        Mouse(self.session, self.address, x, y, click, scroll, self.MOUSE_BREAKER).send_cords()
