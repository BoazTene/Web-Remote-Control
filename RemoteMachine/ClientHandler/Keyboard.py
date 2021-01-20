# from RemoteMachine.ClientHandler.Handler import ClientHandler
# from pynput.keyboard import Key, Listener
#
#
# class Keyboard(Listener):
#     """
#     This class is the Keyboard handler
#     """
#     def __init__(self, session, address):
#         super().__init__(on_press=self.on_press)
#         self.session = session
#         self.address = address
#
#         self.key = self.get_key()
#
#     def on_press(self, key):
#         """
#         This function called each time the client press a key.
#
#         Teh function send to the host the pressed key
#         :param key:
#         :return:
#         """
#         self.session.sendto((ClientHandler.KEYBOARD_BREAKER[0] + key + ClientHandler.KEYBOARD_BREAKER[1]).encode("utf-8"), self.address)
