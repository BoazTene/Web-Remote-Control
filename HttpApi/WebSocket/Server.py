import sys
import time
import threading
import websockets
import asyncio


class Server:
    """
        This class is the main WebSocket server.

        This class makes sure that the client is alive.

        When a remote control starts the client connect to this server.
        The server will ping the client each 2 seconds.
        if the client disconnect the remote control will end and the server will be closed.

        example of to start the server:
            websocket_server = threading.Thread(target=Server, args=(handler, ))
            websocket_server.start()

        check if the server is still alive with:
            websocket_server.is_alive()

        The IS_CLIENT_CONNECTED parameter indicates if the client connected to the server.
    """

    IP = "127.0.0.1"
    PORT = 9898

    IS_CLIENT_CONNECTED = False

    def __init__(self, handler):
        self.handler = handler

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop = asyncio.get_event_loop()
        loop.create_task(self.run())
        loop.run_forever()

    async def run(self):
        self.start_server = websockets.serve(self.new_client_handler, self.IP, self.PORT)
        asyncio.ensure_future(self.start_server)

    def close(self):
        self.handler.close()
        asyncio.get_event_loop().stop()

    def get_state(self):
        try:
            return asyncio.get_event_loop().is_running()
        except AttributeError:
            return False

    async def new_client_handler(self, client, path):
        """
        This function is the handler for new connections.

        This function execute the first and second stages in the HandShake.

        :param client:
        :param path:
        :return:
        """
        print("new Client Connected")
        self.IS_CLIENT_CONNECTED = True

        while True:
            time.sleep(2)
            try:
                pong_waiter = await client.ping()
                await pong_waiter
            except websockets.ConnectionClosed or websockets.ConnectionClosedError:
                # await self.close()
                self.close()
                print("Connection closed")
                break


# if __name__ == "__main__":
#
#     thread = threading.Thread(target=Server, args=(d, ))
#     thread.start()
#
#     while True:
#         pass

