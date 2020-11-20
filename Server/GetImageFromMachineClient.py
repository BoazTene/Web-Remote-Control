import asyncio
import websockets


async def get_image(websocket, path):
    image_base64 = await websocket.recv()