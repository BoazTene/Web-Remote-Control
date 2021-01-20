from RemoteMachine.ClientHandler.CheckAlive import CheckAlive
from RemoteMachine.ClientHandler.GetImage import GetImage
# from RemoteMachine.ClientHandler.Keyboard import Keyboard
# from RemoteMachine.ClientHandler.Mouse import Mouse

import threading


class ClientHandler(threading.Thread):
    """
    This class is the api for the client.
    """

    MAX_IMAGE_DGRAM = 2 ** 16 - 64
    IMAGE_BREAKER = ["<start>", "<end>"]
    ALIVE_CHECK_BREAKER = ["<check-alive>", "<check-alive>"]
    KEYBOARD_BREAKER = ["<key-s>", "<key-e>"]
    MOUSE_BREAKER = ["<mouse-s>", "<mouse-e>"]
    BREAKERS = [IMAGE_BREAKER, ALIVE_CHECK_BREAKER, KEYBOARD_BREAKER, MOUSE_BREAKER]

    def __init__(self, session, address):
        super().__init__()
        self.address = address
        self.session = session

        self.image = "None"

    def get_data(self):
        """
        This function recv the max amount of bytes from the host
        """
        return self.session.recvfrom(self.MAX_IMAGE_DGRAM)

    def find_start_breaker(self, data):
        """
        :data: str

        This function returns all the start breakers in data
        """

        start_breakers = [breaker[0] for breaker in self.BREAKERS]
        return [breaker for breaker in start_breakers if breaker in data]

    @staticmethod
    def find_end_breaker(start_breaker, data):
        """
        This function returns true if the end breaker in data

        :param start_breaker: The start breaker of the searched end breaker
        :param data: str
        :return: bool
        """
        end_breaker = ClientHandler.BREAKERS[[breaker[0] for breaker in ClientHandler.BREAKERS].index(start_breaker)][1]
        return True if end_breaker in data else False

    def get_image(self, data):
        """
        This function call the get_image handler
        :param data:
        :return:
        """

        get_image = GetImage(self.session, self.address, data, self.BREAKERS, self.MAX_IMAGE_DGRAM)
        get_image.run()
        self.image = get_image.image

    def check_alive(self, address):
        """
        This function call the check alive handler
        """
        check_alive = CheckAlive(self.session, address, self.ALIVE_CHECK_BREAKER)
        check_alive.send_alive_ok()

    def keyboard(self):
        """
        This function call the keyboard handler

        :return:
        """

        pass

    def mouse(self):
        """
        This function call the mouse handler

        :return:
        """
        pass

    def run(self):
        """
        This function listens to incoming messages and acting by the messages
        """
        while True:
            data = self.get_data()
            start_breakers = self.find_start_breaker(data[0].decode('utf-8'))
            print(start_breakers)
            for i in start_breakers:
                print(i)
                if i == self.IMAGE_BREAKER[0]:
                    self.get_image(data[0])
                elif i == self.ALIVE_CHECK_BREAKER[0]:
                    self.check_alive(data[1])
