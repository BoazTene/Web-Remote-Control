from Images.ScreenShot import ScreenShot
from Images.ConvrtToBase64 import ConvertImageToBase64


# This class handles the Remote Control
class RemoteControl:
    def __init__(self, s):
        self.s = s

    # this function sends a screenshot to the server
    def send_image(self):
        screen_shot = ScreenShot()
        screen_shot.capture()
        screen_shot.save()
        image = ConvertImageToBase64(screen_shot.buffered).convert()

        self.s.send(image)

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

