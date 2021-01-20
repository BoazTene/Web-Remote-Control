import time


class CountTime:
    """
    This class counts time
    """

    def __init__(self):
        self.start = time.time()

    def get_pass_time(self):
        """
        This function return the time passed from the point the instance was made.
        :return:
        """
        return time.time() - self.start
