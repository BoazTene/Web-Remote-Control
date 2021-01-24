import win32api, win32con


class Mouse:
    def __init__(self, session, address, data, mouse_breaker):
        self.session = session
        self.address = address
        
        self.x, self.y = self.cords_from_data(data)

        self.MOUSE_BRAKER = mouse_breaker

    def cords_from_data(self, data):
        return data.split(self.MOUSE_BRAKER[0])[1].split(self.MOUSE_BRAKER[1])[0].split(",")

    def set_pos(self):
        win32api.SetCursorPos((self.x, self.y))

    def click(self):
        self.set_pos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

