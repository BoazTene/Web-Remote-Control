from RemoteMachine.ClientHandler.Handler import ClientHandler
import pyautogui


class Keyboard:
    """
    This class called each time the host sends a key to press.
    """
    def __init__(self, session, address, data):
        self.session = session
        self.address = address
        self.data = data.decode("utf-8")

        self.key = self.get_key()

    def get_key(self):
        """
        This function return the key the server would like to press.
        """
        return self.data.replace(ClientHandler.KEYBOARD_BREAKER[0], "").replace(ClientHandler.KEYBOARD_BREAKER[1], "")

    def press_key(self):
        """
        This function press the key stored in the key
        """
        pyautogui.press(self.key)
