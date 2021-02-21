from .KeyNotFound import KeyNotFound
import win32api
import win32con
import threading
import time


class Keyboard:
    """
    This class is the keyboard api.
    The api build on the win32api.
    """
    VK_CODE = {'Backspace': 0x08,
               'Tab': 0x09,
               'clear': 0x0C,
               'Enter': 0x0D,
               'Shift': 0x10,
               'ctrl': 0x11,
               'Alt': 0x12,
               'Pause': 0x13,
               'CapsLock': 0x14,
               'Escape': 0x1B,
               ' ': 0x20,
               'PageUp': 0x21,
               'PageDown': 0x22,
               'End': 0x23,
               'Home': 0x24,
               'ArrowLeft': 0x25,
               'ArrowUp': 0x26,
               'ArrowRight': 0x27,
               'ArrowDown': 0x28,
               'select': 0x29,
               'print': 0x2A,
               'execute': 0x2B,
               'PrintScreen': 0x2C,
               'Insert': 0x2D,
               'Delete': 0x2E,
               'Help': 0x2F,
               '0': 0x30,
               '1': 0x31,
               '2': 0x32,
               '3': 0x33,
               '4': 0x34,
               '5': 0x35,
               '6': 0x36,
               '7': 0x37,
               '8': 0x38,
               '9': 0x39,
               'a': 0x41,
               'b': 0x42,
               'c': 0x43,
               'd': 0x44,
               'e': 0x45,
               'f': 0x46,
               'g': 0x47,
               'h': 0x48,
               'i': 0x49,
               'j': 0x4A,
               'k': 0x4B,
               'l': 0x4C,
               'm': 0x4D,
               'n': 0x4E,
               'o': 0x4F,
               'p': 0x50,
               'q': 0x51,
               'r': 0x52,
               's': 0x53,
               't': 0x54,
               'u': 0x55,
               'v': 0x56,
               'w': 0x57,
               'x': 0x58,
               'y': 0x59,
               'z': 0x5A,
               'numpad_0': 0x60,
               'numpad_1': 0x61,
               'numpad_2': 0x62,
               'numpad_3': 0x63,
               'numpad_4': 0x64,
               'numpad_5': 0x65,
               'numpad_6': 0x66,
               'numpad_7': 0x67,
               'numpad_8': 0x68,
               'numpad_9': 0x69,
               'multiply_key': 0x6A,
               'add_key': 0x6B,
               'separator_key': 0x6C,
               'subtract_key': 0x6D,
               'decimal_key': 0x6E,
               'divide_key': 0x6F,
               'F1': 0x70,
               'F2': 0x71,
               'F3': 0x72,
               'F4': 0x73,
               'F5': 0x74,
               'F6': 0x75,
               'F7': 0x76,
               'F8': 0x77,
               'F9': 0x78,
               'F10': 0x79,
               'F11': 0x7A,
               'F12': 0x7B,
               'F13': 0x7C,
               'F14': 0x7D,
               'F15': 0x7E,
               'F16': 0x7F,
               'F17': 0x80,
               'F18': 0x81,
               'F19': 0x82,
               'F20': 0x83,
               'F21': 0x84,
               'F22': 0x85,
               'F23': 0x86,
               'F24': 0x87,
               'NumLock': 0x90,
               'ScrollLock': 0x91,
               'left_shift': 0xA0,
               'right_shift ': 0xA1,
               'Control': 0xA2,
               'right_control': 0xA3,
               'left_menu': 0xA4,
               'right_menu': 0xA5,
               'BrowserBack': 0xA6,
               'BrowserForward': 0xA7,
               'BrowserRefresh': 0xA8,
               'BrowserStop': 0xA9,
               'BrowserSearch': 0xAA,
               'BrowserFavorites': 0xAB,
               'browser_start_and_home': 0xAC,
               'AudioVolumeMute': 0xAD,
               'AudioVolumeDown': 0xAE,
               'AudioVolumeUp': 0xAF,
               'MediaTrackNext': 0xB0,
               'MediaTrackPrevious': 0xB1,
               'MediaStop': 0xB2,
               'MediaPlayPause': 0xB3,
               'LaunchMail': 0xB4,
               'LaunchMediaPlayer': 0xB5,
               'LaunchApplication1': 0xB6,
               'LaunchApplication2': 0xB7,
               'KanaMode': 0xF6,
               'CrSel': 0xF7,
               'ExSel': 0xF8,
               'Play': 0xFA,
               'ZoomToggle': 0xFB,
               'Clear': 0xFE,
               '+': 0xBB,
               ',': 0xBC,
               '-': 0xBD,
               '.': 0xBE,
               '/': 0xBF,
               '`': 0xC0,
               ';': 0xBA,
               '[': 0xDB,
               '\\': 0xDC,
               ']': 0xDD,
               "'": 0xDE}

    hold_keys = {}

    def __init__(self):
        hold_key_thread = threading.Thread(target=self.hold_key_handler)
        hold_key_thread.daemon = True
        hold_key_thread.start()

    def press_key(self, key):
        """
        This function press a given key
        :param key:
        :return:
        """

        try:
            win32api.keybd_event(self.VK_CODE[key], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        except KeyError:

            raise KeyNotFound("You used unrecognized key", "Please only use keys from this list: %s" % self.VK_CODE)

    def key_combination(self, *args):
        """
        This function press a key combination.
        :param args:
        :return:
        """

        # press all the giving keys
        for key in args:
            try:
                win32api.keybd_event(self.VK_CODE[key], 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
                time.sleep(.05)
            except Exception:
                pass
        time.sleep(.05)

        # release all the giving keys
        for key in args:
            try:
                win32api.keybd_event(self.VK_CODE[key], 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(.05)
            except Exception:
                pass

    def hold_key_handler(self):
        '''
            press and hold. Do NOT release.
            accepts as many arguments as you want.
            e.g. pressAndHold('left_arrow', 'a','b').
        '''

        while True:
            for i in list(self.hold_keys):
                win32api.keybd_event(self.VK_CODE[i], 0, 0, 0)
                time.sleep(.05)

    def remove_key_from_holder(self, key):
        """
        This function release key from being pressed.

        :param key:
        :return:
        """

        try:
            del self.hold_keys[key]
        except KeyError:
            pass

    def add_new_key_to_hold(self, key):
        """
        This function start holding key.
        :param key:
        :return:
        """
        self.hold_keys[key] = self.VK_CODE[key]

