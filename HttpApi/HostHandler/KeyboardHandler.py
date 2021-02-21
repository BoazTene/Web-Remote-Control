from HttpApi.HostHandler.CheckAlive import CheckAlive
from HttpApi.HostHandler.Keyboard import Keyboard
import threading


class KeyboardHandler(threading.Thread):
    """
    This class is the Keyboard handler.
    """

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

    def check_alive_recv(self):
        """
        This function is used to tell the check alive class that the client received to the ok message.
        :return:
        """
        print("Keyboard recv")
        self.check_alive.recv_ok = True

    def keyboard(self, data, combination=True):
        """
        This function called each time the Host receives a key to press,
        in addition this function both get the key and press it.

        :param data:
        :return:
        """

        keyboard = Keyboard(self.session, self.address, data)

        try:
            if keyboard.combination:
                keyboard.key_combination(*keyboard.key.split("**"))
            else:
                keyboard.press_key(keyboard.key)
        except Exception:
            pass

    def close(self):
        self.session.close()

    def run(self):
        """
        This function listens to incoming keyboard messages and acting by the messages
        """

        try:
            while True:
                data = self.get_data()
                start_breakers = self.find_start_breakers(data[0].decode("utf-8"))
                print(data[0])
                for i in start_breakers:
                    if i == self.KEYBOARD_BREAKER[0]:
                        self.keyboard(data[0].decode("utf-8"))
                    elif i == self.ALIVE_CHECK_BREAKER[0]:
                        self.check_alive_recv()
        except Exception:
            return
