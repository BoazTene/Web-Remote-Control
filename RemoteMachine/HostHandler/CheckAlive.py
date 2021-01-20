from eventlet.timeout import Timeout
# from RemoteMachine.HostHandler.Handler import HostHandler
from time import sleep
import threading


class CheckAlive(threading.Thread):
    TIMEOUT = 5
    DELAY = 10

    def __init__(self, session, address, alive_check_breaker):
        super().__init__()
        self.session = session
        self.address = address

        self.ALIVE_CHECK_BREAKER = alive_check_breaker

        self.timeout = None
        self.recv_ok = False

    def send_check_alive(self):
        self.session.sendto(self.ALIVE_CHECK_BREAKER[0], self.address)

    def start_timeout(self):
        return Timeout(self.TIMEOUT, TimeoutError)

    def stop_timeout(self):
        self.timeout.cancel()

    def run(self):
        while True:
            sleep(self.DELAY)
            self.timeout = self.start_timeout()
            try:
                self.send_check_alive()
                while True:
                    if self.recv_ok:
                        self.recv_ok = False
                        self.stop_timeout()
                        continue
            except Exception:
                print("Disconnect")
                self.stop_timeout()
                return




