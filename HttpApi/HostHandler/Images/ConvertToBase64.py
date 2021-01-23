import base64


# This class convert image to base64
class ConvertImageToBase64:
    def __init__(self, buffered):
        self.buffered = buffered

    def convert(self):
        return base64.b64encode(self.buffered.getvalue())

    @staticmethod
    def split_image(image_base64, width):
        return [image_base64[i:i + width] for i in range(0, len(image_base64), width)]
    
