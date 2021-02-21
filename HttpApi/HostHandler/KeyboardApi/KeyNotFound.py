class KeyNotFound(Exception):
    """
        Raised when unrecognized key is being asked to press.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the eror
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
