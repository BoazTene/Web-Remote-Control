import base64


# This class convert image to base64
class ConvertImageToBase64:
    def __init__(self, buffered):
        self.buffered = buffered

    def convert(self):
        return base64.b64encode(self.buffered.getvalue())