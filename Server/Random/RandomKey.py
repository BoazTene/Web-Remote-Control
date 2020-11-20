import random
import string


# This class generates a random key for the remote handshake
class RandomKey:
    def __init__(self):
        self.LOWEST_LENGTH = 10
        self.HIGHEST_LENGTH = 10

        self.length = self.random_key_length()

        self.key = self.random_key()

    # generating the key
    def random_key(self):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(self.length))

    # generating the key length
    def random_key_length(self):
        return random.randint(self.LOWEST_LENGTH, self.HIGHEST_LENGTH)