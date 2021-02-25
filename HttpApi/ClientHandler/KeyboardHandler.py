from HttpApi.ClientHandler.CheckAlive import CheckAlive
from HttpApi.ClientHandler.Keyboard import Keyboard
import threading
from multiprocessing import Process


class KeyboardHandler(threading.Thread):
    """
        Some of the breakers can have special attributes.

        keyboard:
            <key-s>(h=t/f|c-=t/f)<key-e>

    """

    IMAGE_BREAKER = ["<start>", "<end>"]
    ALIVE_CHECK_BREAKER = ["<check-alive>"]
    KEYBOARD_BREAKER = ["<key-s>", "<key-e>"]
    MOUSE_BREAKER = ["<mouse-s>", "<mouse-e>"]
    BREAKERS = [IMAGE_BREAKER, ALIVE_CHECK_BREAKER, KEYBOARD_BREAKER, MOUSE_BREAKER]

    def __init__(self, session, address):
        super(KeyboardHandler, self).__init__()

        self.session = session
        self.address = address

    def keyboard(self, key, hold=False, combination=False):
        """
        This function called each time the Host receives a key to press,
        in addition this function both get the key and press it.

        :param hold:
        :param combination:
        :param key:
        :param data:
        :return:
        """

        keyboard = Keyboard(self.session, self.address, key, self.KEYBOARD_BREAKER)
        print(hold, combination)
        if not combination:
            keyboard.send_key_press()
        else:
            keyboard.send_combination()

    def close(self):
        self.session.close()

    def get_data(self):
        """
        This function recv the max amount of bytes from the host
        """
        return self.session.recvfrom(1024)

    def find_start_breakers(self, data):
        """
        :data: str

        This function returns all the start breakers in data
        """
        start_breakers = [breaker[0] for breaker in self.BREAKERS]
        return [breaker for breaker in start_breakers if breaker in data]

    def check_alive(self, address):
        """
        This function call the check alive handler
        """
        check_alive = CheckAlive(self.session, address, self.ALIVE_CHECK_BREAKER)
        check_alive.send_alive_ok()

    def run(self):
        """
       This function listens to incoming keyboard messages and acting by the messages
       """
        try:
            while True:
                data = self.get_data()
                start_breakers = self.find_start_breakers(data[0].decode("utf-8"))

                for i in start_breakers:
                    if i == self.KEYBOARD_BREAKER[0]:
                        self.keyboard(data[0].decode("utf-8"))
                    elif i == self.ALIVE_CHECK_BREAKER[0]:
                        self.check_alive(data[1])
        except Exception:
            return
