import threading


class GetImage(threading.Thread):
    def __init__(self, session, address):
        super().__init__()
        self.address = address
        self.session = session
        self.MAX_IMAGE_DGRAM = 2 ** 16 - 64
        self.images = "Image"
        self.old_image = ""

    def get_chunk(self):
        data, addr = self.session.recvfrom(self.MAX_IMAGE_DGRAM)
        return data

    @staticmethod
    def check_end_transmit(data):
        if "<end>" in data.decode("utf-8"):
            return True
        else:
            return False

    def add_image(self, image):
        image = image.decode("utf-8")
        image = image.split('|')

        if len(image) == 0:
            return self.old_image.encode("utf-8")
        elif len(image) == 1:
            if image[0].split(",")[0] != "''":
                return (self.old_image + str("".join(image[0].split(',')[0]))).encode("utf-8")
            # else:
            #     return self.old_image[:int(image[0].split(',')[1])]

        new_image = self.old_image

        for i in range(len(image)):
            if i == len(image)-1 and image[i].split(",")[0] == "''":
                new_image = new_image[:int(image[i].split(",")[1])]
            elif i == len(image)-1:
                new_image = new_image + image[i]
            else:
                new_image = new_image[:int(image[i].split(",")[1])] + str(image[i].split(",")[0]) +  \
                            new_image[int(image[i].split(",")[1]) + (len(image[i].split(",")[0])-2):]

        return new_image.encode("utf-8")

    def run(self):
        while True:
            data = self.get_chunk()
            if "<start>" in data.decode("utf-8"):
                image = data
                while True:
                    data = self.get_chunk()
                    image += data
                    if GetImage.check_end_transmit(data):
                        image = image.split(b"<start>")[1].split(b"<end>")[0]

                        # image = self.add_image(image)
                        self.images = image
                        self.old_image = image.decode("utf-8")
                        break
            else:
                print(data, "35")

