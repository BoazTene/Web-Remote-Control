from pynput.keyboard import Key, Listener


class Keyboard:
    """
    This class is the Keyboard handler
    """
    def __init__(self, session, address, key, keyboard_breaker):
        super().__init__()

        self.session = session
        self.address = address

        self.KEYBOARD_BREAKER = keyboard_breaker
        self.key = key

    def send(self):
        """
        This function called each time the client press a key.

        Teh function send to the host the pressed key
        :param key:
        :return:
        """
        print((self.KEYBOARD_BREAKER[0] + str(self.key) + self.KEYBOARD_BREAKER[1]).encode("utf-8"))
        self.session.sendto((self.KEYBOARD_BREAKER[0] + str(self.key) + self.KEYBOARD_BREAKER[1]).encode("utf-8"), self.address)
