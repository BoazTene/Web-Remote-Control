
# This class is used to store a list of all the clients
# The data is stored in a class and not a list because you can save reference to a class and not a list,
# that means that list won't work in multi thread program
class Clients:
    def __init__(self):
        self.data = []