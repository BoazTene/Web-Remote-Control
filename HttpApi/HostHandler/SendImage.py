import math
# import multiprocessing
# import socket
import threading
from HttpApi.HostHandler.Images.ScreenShot import ScreenShot
from HttpApi.HostHandler.Images.ConvertToBase64 import ConvertImageToBase64
from time import sleep
# from multiprocessing import Queue, Process, reduction
# import pickle
# import zlib
import time


class SendImage(threading.Thread):
    """
    This Class sends the screenshots to the client
    """

    IMAGE_BREAKER = ['<start>', '<end>']
    MAX_IMAGE_DGRAM = 2 ** 16 - 64

    def __init__(self, session, address, image_breaker):
        super(SendImage, self).__init__()

        self.session = session
        self.address = address

        self.screenshot = ScreenShot()

        self.IMAGE_BREAKER = image_breaker

        self.start_capture()

    def start_capture(self):
        """
        This function start capturing images
        """
        self.screenshot.start_capture()

    def image_to_base64(self):
        """
        This function encode the image to base64
        """
        return ConvertImageToBase64(self.screenshot.buffered).convert()

    def number_of_chunks(self, image):
        """
        This function returns the number of chunks needed to send the image
        """
        return math.ceil(len(image) / self.MAX_IMAGE_DGRAM)

    def send_chunk(self, data):
        """
        This function used to send a chunk of the image to the client
        """
        self.session.sendto(data, self.address)

    def send_image(self):
        """
        This function sends a whole image
        """
        self.screenshot.save()
        image = self.image_to_base64()

        number_of_chunks = self.number_of_chunks(image)

        array_pos_start = 0

        self.send_chunk(self.IMAGE_BREAKER[0].encode("utf-8"))

        while number_of_chunks:
            array_pos_end = min(len(image), array_pos_start + self.MAX_IMAGE_DGRAM)

            self.send_chunk(image[array_pos_start:array_pos_end])

            sleep(0.05)
            array_pos_start = array_pos_end

            number_of_chunks -= 1

        self.send_chunk(self.IMAGE_BREAKER[1].encode("utf-8"))

    def run(self):
        """
        This function is the main function.
        This function called when calling to .start()
        """

        try:
            while True:
                self.send_image()
        except Exception:
            return
