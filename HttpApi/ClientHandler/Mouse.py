

class Mouse:
    """
    This class called each time the client move his mouse.

    The class sends the new position of the mouse to the host.
    """
    def __init__(self, session, address, x, y, mouse_breaker):
        self.session = session
        self.address = address
        self.x = x
        self.y = y

        self.MOUSE_BREAKER = mouse_breaker

    def send_cords(self):
        """
        This function sends a string which contains the x, y cords of the new mouse
        """
        data = "%s%s,%s%s" % (self.MOUSE_BREAKER[0], self.x, self.y, self.MOUSE_BREAKER[1])
        self.session.sendto(data.encode("utf-8"), self.address)
