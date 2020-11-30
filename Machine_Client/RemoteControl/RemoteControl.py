from Images.ScreenShot import ScreenShot
from Images.ConvertToBase64 import ConvertImageToBase64


# This class handles the Remote Control
class RemoteControl:
    def __init__(self, s, addr):
        self.s = s
        self.addr = addr

    # this function sends a screenshot to the server
    def send_image(self):
        screen_shot = ScreenShot()
        screen_shot.capture()
        screen_shot.save()
        image = ConvertImageToBase64(screen_shot.buffered).convert()
        split_image = ConvertImageToBase64.split_image(image, int(len(image)/700))

        # self.s.sendto(b"<start>", self.addr)
        #
        # for i in split_image:
        #     self.s.sendto(i, self.addr)
        #
        # self.s.sendto(b"<start>", self.addr)

        print("Image")

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

