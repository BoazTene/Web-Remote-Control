import threading
from HttpApi.HostHandler.CheckAlive import CheckAlive
from HttpApi.HostHandler.MouseApi import Mouse


class MouseHandler(threading.Thread):
    IMAGE_BREAKER = ["<start>", "<end>"]
    ALIVE_CHECK_BREAKER = ["<check-alive>"]
    KEYBOARD_BREAKER = ["<key-s>", "<key-e>"]
    MOUSE_BREAKER = ["<mouse-s>", "<mouse-e>"]
    BREAKERS = [IMAGE_BREAKER, ALIVE_CHECK_BREAKER, KEYBOARD_BREAKER, MOUSE_BREAKER]

    def __init__(self, session, address):
        super().__init__()
        self.session = session
        self.address = address

        # self.check_alive = CheckAlive(self.session, self.address, self.ALIVE_CHECK_BREAKER)
        # self.check_alive.start()

    def get_data(self):
        return self.session.recvfrom(1024)

    def find_start_breakers(self, data):
        """
        :data: str

        This function returns all the start breakers in data
        """
        start_breakers = [breaker[0] for breaker in self.BREAKERS]
        return [breaker for breaker in start_breakers if breaker in data]

    def mouse(self, data):
        Mouse(data)

    def run(self):
        # try:
        while True:
            data = self.get_data()
            print(data[0])
            start_breakers = self.find_start_breakers(data[0].decode("utf-8"))

            for i in start_breakers:
                if i == self.MOUSE_BREAKER[0]:
                    self.mouse(data[0].decode('utf-8'))
                elif i == self.ALIVE_CHECK_BREAKER[0]:
                    pass
        # except Exception as e:
        #     print(e)
