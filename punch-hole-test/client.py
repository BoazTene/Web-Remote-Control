import socket
import struct
from threading import Thread

def bytes_to_addr(addr):
    return struct.unpack('BBBB', socket.inet_aton(addr))

def udp_client(server):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.sendto(b'', server)
    data, _ = soc.recvfrom(6)
    peer = data.decode('utf 8')
    print('peer:', *peer)

    Thread(target=soc.sendto, args=(b'hello', peer)).start()
    data, addr = soc.recvfrom(1024)
    print('{}:{} says {}'.format(*addr, data))


server_addr = ('server_ip', 4000) # the server's  public address
udp_client(server_addr)