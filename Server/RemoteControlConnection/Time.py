import time


# This class counts time
class CountTime:
    def __init__(self):
        self.start = time.time()

    def get_pass_time(self):
        return time.time() - self.start