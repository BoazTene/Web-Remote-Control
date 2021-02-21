from pynput.keyboard import Key, Listener


class Keyboard:
    """
    This class is the Keyboard handler
    """
    combinations = {
        'cut': "control&&x",
        'copy': 'control&&c',
        'paste': 'Control&&v',
    }

    def __init__(self, session, address, key, keyboard_breaker):
        super().__init__()

        self.session = session
        self.address = address

        self.KEYBOARD_BREAKER = keyboard_breaker
        self.key = key

    def send_key_press(self):
        """
        The function send the host the pressed key

        :param key:
        :return:
        """
        self.session.sendto((self.KEYBOARD_BREAKER[0] + "(h=f|c=f)" + str(self.key) +
                             self.KEYBOARD_BREAKER[1]).encode("utf-8"),
                            self.address)

    def send_hold_key(self):
        """
            The function send the host key to hold.
            :param key:
            :return:
        """
        pass

    def send_combination(self):
        """
            The function send the host key combination

            :param key:
            :return:
        """
        print((self.KEYBOARD_BREAKER[0] + "(h=f|c=t)" + str(self.key) +
                             self.KEYBOARD_BREAKER[1]).encode("utf-8"))
        self.session.sendto((self.KEYBOARD_BREAKER[0] + "(h=f|c=t)" + str(self.key) +
                             self.KEYBOARD_BREAKER[1]).encode("utf-8"),
                            self.address)
