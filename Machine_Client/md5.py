import hashlib


class Md5:
    def __init__(self, string):
        self.string = string

    def encrypt(self):
        return hashlib.md5(self.string.encode("utf-8")).hexdigest()