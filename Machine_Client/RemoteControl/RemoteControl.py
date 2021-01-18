import math
import zlib
# from RemoteControl.Handshake import *
from Machine_Client.Images.ScreenShot import ScreenShot
from Machine_Client.Images.ConvertToBase64 import ConvertImageToBase64
from Machine_Client.Images.ImageDifference import ImageDifferences
import time


# This class handles the Remote Control
class RemoteControl:
    def __init__(self, s, addr):
        self.s = s
        self.addr = addr
        # print("\n\n" + addr + "\n\n")
        self.old_image = ""
        self.MAX_IMAGE_DGRAM = 2 ** 16 - 64
        self.screen_shot = ScreenShot()
        self.screen_shot.start_capture()

    # this function sends a screenshot to the server
    def send_image(self):
        self.screen_shot.save()

        image = ConvertImageToBase64(self.screen_shot.buffered).convert()
        print(len(image))
        print(len(image) / self.MAX_IMAGE_DGRAM)
        num_of_segments = math.ceil(len(image) / self.MAX_IMAGE_DGRAM)
        # split_image = ConvertImageToBase64.split_image(image, )
        # print("\n\n" + self.addr + "\n\n")
        self.s.sendto(b"<start>", self.addr)
        array_pos_start = 0
        while num_of_segments:
            array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
            time.sleep(0.00001)
            array_pos_start = array_pos_end
            num_of_segments -= 1

        self.s.sendto(b"<end>", self.addr)

        self.old_image = self.screen_shot.buffered
        print("image")
        return

        # if self.old_image is None:
        #     image = ConvertImageToBase64(screen_shot.buffered).convert()
        #     print(len(image))
        #     print(len(image) / self.MAX_IMAGE_DGRAM)
        #     num_of_segments = math.ceil(len(image) / self.MAX_IMAGE_DGRAM)
        #     # split_image = ConvertImageToBase64.split_image(image, )
        #     # print("\n\n" + self.addr + "\n\n")
        #     self.s.sendto(b"<start>", self.addr)
        #     array_pos_start = 0
        #     while num_of_segments:
        #         array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
        #         self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
        #         time.sleep(0.00001)
        #         array_pos_start = array_pos_end
        #         num_of_segments -= 1
        #
        #     self.s.sendto(b"<end>", self.addr)
        #
        #     self.old_image = screen_shot.buffered
        #     print("image")
        #     return

        if self.old_image == "":
            image = ConvertImageToBase64(screen_shot.buffered).convert()
            print(len(image))
            print(len(image) / self.MAX_IMAGE_DGRAM)
            num_of_segments = math.ceil(len(image) / self.MAX_IMAGE_DGRAM)
            # split_image = ConvertImageToBase64.split_image(image, )
            # print("\n\n" + self.addr + "\n\n")
            self.s.sendto(b"<start>", self.addr)
            array_pos_start = 0
            while num_of_segments:
                array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
                self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
                time.sleep(0.00001)
                array_pos_start = array_pos_end
                num_of_segments -= 1

            self.s.sendto(b",0<end>", self.addr)

            self.old_image = screen_shot.buffered
            return

        image_difference = ImageDifferences(ConvertImageToBase64(screen_shot.buffered).convert(),
                                            ConvertImageToBase64(self.old_image).convert())

        image_difference.sub()

        # print(ConvertImageToBase64(screen_shot.buffered).convert())
        image = str(image_difference).encode('utf-8') + b"<end>"
        print(image)
        self.s.sendto(b"<start>", self.addr)

        array_pos_start = 0
        num_of_segments = math.ceil(len(str(image)) / self.MAX_IMAGE_DGRAM)

        while num_of_segments:
            array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(image[array_pos_start:array_pos_end], self.addr)
            time.sleep(0.001)
            array_pos_start = array_pos_end
            num_of_segments -= 1

        time.sleep(0.00001)
        # self.s.sendto(b"<end>", self.addr)

        self.old_image = screen_shot.buffered
        print(image)
        # print(screen_shot.buffered.getvalue())
        # exit()

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
