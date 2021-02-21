from HttpApi.ClientHandler.CheckAlive import CheckAlive
from HttpApi.ClientHandler.GetImage import GetImage
from HttpApi.ClientHandler.Keyboard import Keyboard
from HttpApi.ClientHandler.Mouse import Mouse
from HttpApi.ClientHandler.HandShake.NewPort import NewPort
import time
import threading


class ClientHandler(threading.Thread):
    """
    This class is the http api for the client.
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

        self.keyboard_session = None
        self.keyboard_address = None

        self.recv = []

        self.image = "None"

        self.time = 0
        self.images_num = 0

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
        self.recv.extend(get_image.recv)

    def close(self):
        self.session.close()

    def check_alive(self, address):
        """
        This function call the check alive handler
        """
        print("damn")
        check_alive = CheckAlive(self.session, address, self.ALIVE_CHECK_BREAKER)
        check_alive.send_alive_ok()

    def keyboard(self, key):
        """
        This function call the keyboard handler

        :return:
        """

        Keyboard(self.keyboard_session, self.keyboard_address, key, self.KEYBOARD_BREAKER).send()

    def mouse(self, x, y):
        """
        This function call the mouse handler

        :return:
        """
        # Mouse(self.session, self.address, x, y, self.MOUSE_BREAKER).send_cords()

    def open_new_port(self):
        new_port = NewPort(self.session, self.address)
        return new_port.run()

    def run(self):
        """
        This function listens to incoming messages and acting by the messages
        """

        # self.keyboard_session, self.keyboard_address = self.open_new_port()
        starting_time = 0
        num = 1
        try:
            while True:
                data = self.get_data()
                self.address = data[1]
                start_breakers = self.find_start_breaker(data[0].decode('utf-8'))
                # print(start_breakers)
                # print(self.recv)
                # try:
                #     print("Fps: %s, Number of Images: %s, Time: %s" % (self.images_num / (time.perf_counter() - starting_time) , self.images_num, (time.perf_counter() - starting_time)))
                # except ZeroDivisionError:
                #     print("Fps: 0")

                for i in start_breakers, self.recv:
                    # print(i)
                    if self.IMAGE_BREAKER[0] in i:

                        self.get_image(data[0])

                        if starting_time == 0:
                            if num != 50:
                                num += 1
                            else:
                                starting_time = time.perf_counter()
                                self.images_num += 1
                        else:
                            # self.time += time.perf_counter() - starting_time
                            self.images_num += 1

                    elif self.ALIVE_CHECK_BREAKER[0] in i:
                        self.check_alive(data[1])

                self.recv = []
        except Exception:
            return

