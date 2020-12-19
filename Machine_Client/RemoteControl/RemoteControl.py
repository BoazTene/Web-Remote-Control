import math
import zlib
from Images.ScreenShot import ScreenShot
from Images.ConvertToBase64 import ConvertImageToBase64
from Images.ImageDifference import ImageDifferences
import time


# This class handles the Remote Control
class RemoteControl:
    def __init__(self, s, addr):
        self.s = s
        self.addr = addr
        self.old_image = None
        self.MAX_IMAGE_DGRAM = 2**16 - 64

    # this function sends a screenshot to the server
    def send_image(self):
        screen_shot = ScreenShot()
        screen_shot.capture()
        screen_shot.save()

        if self.old_image is None:
            image = ConvertImageToBase64(screen_shot.buffered).convert()
            print(len(image))
            print(len(image) / self.MAX_IMAGE_DGRAM)
            num_of_segments = math.ceil(len(image) / self.MAX_IMAGE_DGRAM)
            # split_image = ConvertImageToBase64.split_image(image, )

            self.s.sendto(b"<start>", self.addr)
            array_pos_start = 0
            while num_of_segments:
                array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
                self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
                time.sleep(0.00001)
                array_pos_start = array_pos_end
                num_of_segments -= 1

            self.s.sendto(b"<end>", self.addr)

            self.old_image = screen_shot.buffered
            print("image")
            return

        print("d")
        image_difference = ImageDifferences(screen_shot.buffered, self.old_image)
        print("d")

        image_difference.sub()
        print("d")

        image = str(image_difference).encode('utf-8') + b"<end>"
        print("d")

        self.s.sendto(b"<start>", self.addr)

        array_pos_start = 0
        num_of_segments = math.ceil(len(str(image)) / self.MAX_IMAGE_DGRAM)
        print(len(str(image)))
        while num_of_segments:
            array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
            time.sleep(0.001)
            array_pos_start = array_pos_end
            num_of_segments -= 1

        time.sleep(0.00001)
        # self.s.sendto(b"<end>", self.addr)

        self.old_image = screen_shot.buffered

        print("Image")
        exit()

    # This function exec an command
    # move mouse, click, keyboard press
    def command(self, command):
        pass

    # this function checks the connection
    def check_connection(self):
        while True:
            data = self.s.recv(1024).decode("utf-8")
            if data == "disconnected":
                print("disconnected")
                return
            elif data != "Alive Check":
                # that means that the server send a command
                self.command(data)

