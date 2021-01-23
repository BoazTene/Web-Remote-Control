# from HttpApi.ClientHandler.Handler import ClientHandler

class CheckAlive:
    """
    This class called each time the server checks if the client alive.
    """
    def __init__(self, session, address, breaker):
        self.session = session
        self.address = address

        self.ALIVE_CHECK_BREAKER = breaker

    def send_alive_ok(self):
        """
         Sends an ok message to the server
        """
        self.session.sendto(self.ALIVE_CHECK_BREAKER[0].encode("utf-8"), self.address)
