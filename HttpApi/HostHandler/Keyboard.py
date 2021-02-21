import time
from HttpApi.HostHandler.KeyboardApi import Keyboard as KeyboardApi
from HttpApi.ClientHandler.Handler import ClientHandler
import pyautogui
import win32con
import win32api


class Keyboard(KeyboardApi):
    """
    This class called each time the host sends a key to press.
    """

    def __init__(self, session, address, data):
        self.session = session
        self.address = address
        self.data = data

        self.key, self.combination = self.get_key()
        print(self.key)

    def get_key(self):
        """
        This function return the key the server would like to press.
        """
        return self.data.replace(ClientHandler.KEYBOARD_BREAKER[0], "").replace(ClientHandler.KEYBOARD_BREAKER[1], "")\
            .split(")", 1)[1], self.data.replace(ClientHandler.KEYBOARD_BREAKER[0], "").replace(ClientHandler.KEYBOARD_BREAKER[1], "")\
            .split(")", 1)[0].split('c=')[1] == 't'

    # def press_key(self):
    #     """
    #     This function press the key stored in the key
    #     """
    #     # self.key = self.key.lower()
    #
    #     try:
    #         if self.key != " ":
    #             win32api.keybd_event(self.VK_CODE[self.key], 0, 0, 0)
    #             # win32api.keybd_event(self.VK_CODE[self.key], 0, win32con.KEYEVENTF_KEYUP, 0)
    #         else:
    #             win32api.keybd_event(self.VK_CODE['spacebar'], 0, 0, 0)
    #             time.sleep(.05)
    #             # win32api.keybd_event(self.VK_CODE['spacebar'], 0, win32con.KEYEVENTF_KEYUP, 0)
    #     except Exception:
    #         pass