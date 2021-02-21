from io import BytesIO
import d3dshot


# This class takes a screenshot
# You can find the result saves to self.buffered
class ScreenShot:
    def __init__(self, location=None):
        self.location = location
        self.img = None
        self.buffered = BytesIO()
        self.d = d3dshot.create()

    # capture the image
    def start_capture(self):
        self.d.capture(target_fps=60)

    # return Pil of the last image
    def get_last_image(self):
        return self.d.get_latest_frame()

    # this stop the screenshot capture
    def stop(self):
        self.d.stop()

    # saves it to self.buffered
    def save(self):
        try:
            self.buffered = BytesIO()
            self.d.get_latest_frame().save(self.buffered, format="JPEG", quality=70) # , quality=10
        except AttributeError:
            print("NoneType error")



