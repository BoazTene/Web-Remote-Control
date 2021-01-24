# from HttpApi.self.Handler import self


class GetImage:
    """
    This class handles the image receiving.
    It called each time the server start sending image.


    Use:
        After you create an instance of the class you can call the run function,
        when the run function finished the image data will be stored at image
    """
    def __init__(self, session, address, data, breakers, buffer_size):
        self.session = session
        self.address = address
        self.image = data

        self.IMAGE_BREAKER = breakers[0]
        self.BREAKERS = breakers
        self.MAX_IMAGE_DGRAM = buffer_size

        self.recv = []

    def get_chunk(self):
        """
        This function returns a chunk of the image from the server
         """

        data, addr = self.session.recvfrom(self.MAX_IMAGE_DGRAM)

        start_breakers = [breaker[0] for breaker in self.BREAKERS]
        self.recv.extend([breaker for breaker in start_breakers if breaker in data.decode("utf-8")])

        return data

    def find_end_breaker(self, start_breaker, data):
        """
        This function returns true if the end breaker in data

        :param start_breaker: The start breaker of the searched end breaker
        :param data: str
        :return: bool
        """
        return True if self.BREAKERS[0][1] in data else False

    def run(self):
        """
        This the main function it connects all the chunks to image
        """
        if self.find_end_breaker(self.image.decode("utf-8"), self.IMAGE_BREAKER[0]):
            self.image = self.image.split(self.IMAGE_BREAKER[0].encode("utf-8"))[1] \
                .split(self.IMAGE_BREAKER[1].encode("utf-8"))[0]
            return

        while True:
            data = self.get_chunk()
            self.image += data

            if self.IMAGE_BREAKER[1] in data.decode('utf-8'):
                self.image = self.image.split(self.IMAGE_BREAKER[0].encode("utf-8"))[1]\
                    .split(self.IMAGE_BREAKER[1].encode("utf-8"))[0]
                # print(self.recv)
                return
