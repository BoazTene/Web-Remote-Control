import threading


class GetImage(threading.Thread):
    def __init__(self, session, address):
        super().__init__()
        self.address = address
        self.session = session
        self.MAX_IMAGE_DGRAM = 2 ** 16 - 64
        self.images = []

    def get_chunk(self):
        data, addr = self.session.recvfrom(self.MAX_IMAGE_DGRAM)
        return data

    @staticmethod
    def check_end_transmit(data):
        if data.contains("<end>"):
            return True
        else:
            return False

    def run(self):
        while True:
            data = self.get_chunk()
            if data.contains("<start>"):
                image = data
                while True:
                    data = self.get_chunk()
                    image += data
                    if GetImage.check_end_transmit(data):
                        self.images.append(image)
                        break

