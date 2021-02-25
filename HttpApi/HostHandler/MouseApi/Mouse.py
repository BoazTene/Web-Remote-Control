import time

import numpy as np
from HttpApi.HostHandler.KeyboardApi import Keyboard as KeyboardApi
from HttpApi.HostHandler.Handler import HostHandler
import win32api
import win32con


class Mouse:
    """
    This is the Mouse Api you can see the docs in:
        1. https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        2. https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setcursorpos
    """

    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)

    def __init__(self, data):
        self.data = data
        print(0)
        self.x, self.y, self.click, self.direction = self.get_mouse()
        print(0.5)
        self.x = float(self.x)
        self.y = float(self.y)
        self.direction = int(self.direction)

        self.move_mouse()

        if self.click == 'l':
            self.left_button()
        elif self.click == 'r':
            self.right_button()
        elif self.click == "m":
            self.middle_button()
        elif self.click == 's':
            self.scroll()

    def get_mouse(self):
        """
        This function return the key the server would like to press.
        """
        x = self.data.replace(HostHandler.MOUSE_BREAKER[0], "").replace(HostHandler.MOUSE_BREAKER[1], "") \
                   .split(")", 1)[1].split(',')[0]
        y = self.data.replace(HostHandler.MOUSE_BREAKER[0], "").replace(HostHandler.MOUSE_BREAKER[1], "") \
                   .split(")", 1)[1].split(',')[1]
        click = self.data.replace(HostHandler.KEYBOARD_BREAKER[0], "") \
            .replace(HostHandler.KEYBOARD_BREAKER[1], "") \
            .split(")", 1)[0].split("|")[0].split('c=')[1]

        scroll = self.data.replace(HostHandler.KEYBOARD_BREAKER[0], "") \
            .replace(HostHandler.KEYBOARD_BREAKER[1], "") \
            .split(")", 1)[0].split("|")[1].split('s=')[1]

        return x, y, click, scroll

    def move_mouse(self):
        """
        This function move the mouse to the x, y coordinates relative to the last position.

        :return:
        """
        self.x *= self.width
        self.y *= self.height

        self.x = int(self.x)
        self.y = int(self.y)

        win32api.SetCursorPos((self.x, self.y))

    def move_absolute(self):
        """
        This function move the mouse to the x, y coordinates relative to 0,0.

        :return:
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, self.x, self.y, 0, 0)

    def left_button(self):
        """
        Press the left mouse button.

        :return:
        """
        self.x = int(self.x)
        self.y = int(self.y)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)

        time.sleep(.05)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

    def right_button(self):
        """
        Press the right mouse button.
        :return:
        """
        self.x = int(self.x)
        self.y = int(self.y)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.x, self.y, 0, 0)

        time.sleep(.05)

        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.x, self.y, 0, 0)

    def middle_button(self):
        """
        Press the middle mouse button.
        :return:
        """
        self.x = int(self.x)
        self.y = int(self.y)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, self.x, self.y, 0, 0)

        time.sleep(.05)

        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, self.x, self.y, 0, 0)

    def scroll(self):
        """
        Preforms one mouse wheel scroll.

        A positive value int the self.direction indicates that the wheel was rotated forward, away from the user;
        a negative value indicates that the wheel was rotated backward, toward the user.

        :return:
        """

        self.x = int(self.x)
        self.y = int(self.y)

        self.direction = int(self.direction / np.abs(self.direction))  # set the direction to 1 or -1

        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, self.x, self.y, self.direction * 120, 0)
