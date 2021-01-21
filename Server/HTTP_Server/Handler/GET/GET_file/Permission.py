from urllib.parse import quote
from .Data import *


class Permission:
    def __init__(self, path):
        self.path = path
        self.unescape()

    def is_authorized(self):
        if self.path in AUTHORIZED_FILES:
            return True
        else:
            print(self.path, "file")
            return False

    def unescape(self):
        return quote(self.path)