import random
import string


class RandomKey:
    """
    This class generates a random key for the remote handshake.
    """

    LOWEST_LENGTH = 10
    HIGHEST_LENGTH = 10

    def __init__(self):
        self.length = self.random_key_length()

        self.key = self.random_key()

    def random_key(self):
        """
        this function generates a random string
        :return:
        """

        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(self.length))

    def random_key_length(self):
        """
        This function generates the key length
        :return:
        """

        return random.randint(self.LOWEST_LENGTH, self.HIGHEST_LENGTH)