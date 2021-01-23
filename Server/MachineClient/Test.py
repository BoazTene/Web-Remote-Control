import os
import array
import six
import socket
import struct
import hashlib
import base64
import threading
import datetime

OPCODE_TEXT = 0x1

try:
    # If wsaccel is available we use compiled routines to mask data.
    from wsaccel.xormask import XorMaskerSimple

    def _mask(_m, _d):
        return XorMaskerSimple(_m).process(_d)

except ImportError:
    # wsaccel is not available, we rely on python implementations.
    def _mask(_m, _d):
        for i in range(len(_d)):
            _d[i] ^= _m[i % 4]

        if six.PY3:
            return _d.tobytes()
        else:
            return _d.tostring()


def get_masked(data):
    mask_key = os.urandom(4)
    if data is None:
        data = ""

    bin_mask_key = mask_key
    if isinstance(mask_key, six.text_type):
        bin_mask_key = six.b(mask_key)

    if isinstance(data, six.text_type):
        data = six.b(data)

    _m = array.array("B", bin_mask_key)
    _d = array.array("B", data)
    s = _mask(_m, _d)

    if isinstance(mask_key, six.text_type):
        mask_key = mask_key.encode('utf-8')
    return mask_key + s


def ws_encode(data="", opcode=OPCODE_TEXT, mask=1):
    if opcode == OPCODE_TEXT and isinstance(data, six.text_type):
        data = data.encode('utf-8')

    length = len(data)
    fin, rsv1, rsv2, rsv3, opcode = 1, 0, 0, 0, opcode

    frame_header = chr(fin << 7 | rsv1 << 6 | rsv2 << 5 | rsv3 << 4 | opcode)

    if length < 0x7e:
        frame_header += chr(mask << 7 | length)
        frame_header = six.b(frame_header)
    elif length < 1 << 16:
        frame_header += chr(mask << 7 | 0x7e)
        frame_header = six.b(frame_header)
        frame_header += struct.pack("!H", length)
    else:
        frame_header += chr(mask << 7 | 0x7f)
        frame_header = six.b(frame_header)
        frame_header += struct.pack("!Q", length)

    if not mask:
        return frame_header + data
    return frame_header + get_masked(data)


def ws_decode(data):
    """
    ws frame decode.
    :param data:
    :return:
    """
    _data = [ord(character) for character in data]
    length = _data[1] & 127
    index = 2
    if length < 126:
        index = 2
    if length == 126:
        index = 4
    elif length == 127:
        index = 10
    return array.array('B', _data[index:]).tostring()


# connect

def main():


    def conn(c, addr):

        print(addr)
        # handshake

        data = c.recv(1024).decode("utf-8")
        key = data.split("Sec-WebSocket-Key: ")[1].split("\r\nDNT:")[0] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        key = base64.b64encode(hashlib.sha1(key.encode('utf-8')).hexdigest().encode('utf-8'))
        handshake = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: " \
                    "Upgrade\r\nSec-WebSocket-Accept: %s\r\nSec-WebSocket-Extensions: permessage-deflate\r\nServer: Python/3.8 websockets/8.1\r\n\r\n" % (key.decode("utf-8"))


        c.send(handshake.encode("utf-8"))

        response = c.recv(1024)
        print(ws_encode(data = "lahoh"))
        c.send(ws_encode(data = "lahoh"))

        print(data)
        print(handshake)
        # c.send(ws_encode(data='Hello, China!', opcode=OPCODE_TEXT))
        print("lahoh")
        # receive it back
        print('--%s--' % response)

        response = c.recv(1024)

        # c.send(ws_encode(data='Hello, China!', opcode=OPCODE_TEXT))
        print("lahoh")
        # receive it back
        print('--%s--' % response)

        response = c.recv(1024)

        # c.send(ws_encode(data='Hello, China!', opcode=OPCODE_TEXT))
        print("lahoh")
        # receive it back
        print('--%s--' % response)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 1324))
    sock.listen(5)

    while True:
        c, addr = sock.accept()
        threading.Thread(target=conn, args=(c, addr,)).start()




threading.Thread(target=main).start()
# sock.close()

# import asyncio
# import websockets
#
# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(f"< {name}")
#
#     greeting = f"Hello {name}!"
#
#     await websocket.send(greeting)
#     print(f"> {greeting}")
#
# start_server = websockets.serve(hello, "localhost", 1324)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()