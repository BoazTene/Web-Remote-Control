from io import BytesIO
import pyautogui


# This class takes a screenshot
# You can find the result saves to self.buffered
class ScreenShot:
    def __init__(self, location=None):
        self.location = location
        self.img = None
        self.buffered = BytesIO()

    # capture the image
    def capture(self):
        if self.location is None:
            self.img = pyautogui.screenshot()
        else:
            self.img = pyautogui.screenshot(region=self.location)

    # saves it to self.buffered
    def save(self):
        self.img.save(self.buffered, format="JPEG",optimize=True) # , quality=10