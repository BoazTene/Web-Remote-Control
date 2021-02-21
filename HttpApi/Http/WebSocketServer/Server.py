from HttpApi.Http.WebSocketServer.Login import Login
from HttpApi.Http.WebSocketServer.Register import Register
import websockets
import asyncio


class Server:
    """
        This class is the main WebSocket server.

        HandShake:
            1. The web sends 'L/R/I'/'K'/'M' - Image handler, Keyboard handler, Mouse handler to
            2.  The Websockets server response with 'True' or 'False'.
    """

    IP = "127.0.0.1"
    PORT = 1234

    IMAGE_HANDLER = 'I'
    KEYBOARD_HANDLER = 'K'
    MOUSE_HANDLER = "M"

    REGISTER = "R"
    LOGIN = "L"

    OK_RESPONSE = "True"
    FAILURE_RESPONSE = "False"

    image_client = None
    keyboard_client = None
    mouse_client = None

    image_handler = None
    keyboard_handler = None
    mouse_handler = None

    register_handler = None

    def __init__(self):
        server = websockets.serve(self.new_client_handler, self.IP, self.PORT)
        
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

    async def new_client_handler(self, client, path):
        """
        This function is the handler for new connections.

        This function execute the first and second stages in the HandShake.

        :param client:
        :param path:
        :return:
        """

        handler = await client.recv()

        if handler == self.IMAGE_HANDLER:
            await client.send(self.OK_RESPONSE)
            self.image_client = client

        elif handler == self.KEYBOARD_HANDLER:
            await client.send(self.OK_RESPONSE)

            self.keyboard_client = client
        elif handler == self.MOUSE_HANDLER:
            await client.send(self.OK_RESPONSE)

            self.mouse_client = client
        elif handler == self.REGISTER:
            # Registers as host....

            username = await client.recv()
            password = await client.recv()

            if not self.image_handler and not self.keyboard_handler and not self.mouse_handler:
                await client.send(self.FAILURE_RESPONSE)
                return

            register = Register(self.IP, self.PORT, username, password)
            register.register()

            self.register_handler = register

            await client.send(self.OK_RESPONSE)

        elif handler == self.LOGIN:
            # Login to host....

            username = await client.recv()
            password = await client.recv()

            login = Login(self.IP, self.PORT, username, password)
            self.image_handler, self.keyboard_handler, result = login.login()
            print(result)
            if result:
                await client.send(self.OK_RESPONSE)
            else:
                await client.send(self.FAILURE_RESPONSE)
        else:
            await client.send(self.FAILURE_RESPONSE)


if __name__ == "__main__":
    ws = Server()
    asyncio.get_event_loop().run_until_complete(ws.new_client_handler())
    asyncio.get_event_loop().run_forever()