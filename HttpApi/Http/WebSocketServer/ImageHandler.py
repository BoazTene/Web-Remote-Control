import asyncio
import websockets
from websockets import WebSocketServerProtocol


class Handler:
    IMAGE_HANDLER = 'I'
    KEYBOARD_HANDLER = 'K'
    MOUSE_HANDLER = "M"

    OK_RESPONSE = "ok"
    FAILURE_RESPONSE = "err"

    def __init__(self, socket: WebSocketServerProtocol, path):
        self.socket = socket
        self.path = path

    async def run(self):
        while True:
            handler = await self.socket.recv()
            if handler == self.IMAGE_HANDLER:
                await self.socket.send(self.OK_RESPONSE)
            elif handler == self.KEYBOARD_HANDLER:
                await self.socket.send(self.OK_RESPONSE)
            elif handler == self.MOUSE_HANDLER:
                await self.socket.send(self.OK_RESPONSE)
            else:
                await self.socket.send(self.FAILURE_RESPONSE)
