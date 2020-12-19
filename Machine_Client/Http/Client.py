import requests


# This class is the http client
class HttpClient:
    def __init__(self, port):
        self.url = f"localhost:{port}"

    # This method get an image data as base64 and send it to the http server
    def send_image(self, image_data):
        return requests.get(f"{self.url}/image/{image_data}").content

    # This method get a command and send it to the http server
    def send_command(self, command):
        return requests.get(f"{self.url}/command/{command}").content