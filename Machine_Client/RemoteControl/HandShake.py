import socket


# This is the HandShake client
# The Socket object is saved after the HandShake in self.s
# If the HandShake completed successfully the self.hand_shake value is True else its value is False
class HandShake:
    def __init__(self, s, host):
        self.host = host

        self.port, self.key = HandShake.get_port_and_key(s)

        self.hand_shake = False

        print(self.port, self.key)

        self.connect()


        self.send_key()
        print("This code is strong as static and benel with ana zack eating lahoh")

        if self.OK():
            self.send_type()
            if self.OK():
                if self.OK():
                    self.hand_shake = True
                    print("The HandShake completed successfully")
                else:
                    print("The HandShake failed because of the remote client.")
                    return
            else:
                print("Something bad happened.")
        else:
            print("The key isn't correct.")

    # This function gets the identity key from the server and the port of the private server
    @staticmethod
    def get_port_and_key(s):
        while True:
                port = s.recv(1024).decode("utf-8")
                if port != "Alive Check":
                    break
                else:
                    print(port)

        while True:
            key = s.recv(1024).decode("utf-8")
            if key != "Alive Check":
                break
            else:
                print(key)

        return int(port.split("!")[0]), key

    # This function connects to the server
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    # this function send the identity key
    def send_key(self):
        self.s.send(self.key.encode("utf-8"))

        # print(self.s.recv(1024).decode("utf-8"))

    # this function sends that this is a machine client -> m
    def send_type(self):
        self.s.send(b"m")

    # This function checks if Ok arrived
    def OK(self):
        data = self.s.recv(1024).decode("utf-8")

        if data.lower() == 'ok':
            return True
        elif data == "Alive Check":
            return self.OK()
        else:
            print("Failed! " + data)
            return False