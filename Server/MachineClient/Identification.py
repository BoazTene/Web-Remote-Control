from Server.SQL import DataBase


class Identification:
    def __init__(self, creds, length):
        self.creds = creds
        self.db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db")
        self.data = self.db.get_data()
        self.length = length

    def check(self):
        for raw in self.data:
            if self.creds[0] == raw[0]:
                return False

        self.add_raw()
        self.close()
        return True

    def check_remote_client(self):
        index = 0
        for raw in self.data:
            if self.creds[0] == raw[0]:
                return [True, index]
            index += 1

        self.close()
        return [False, None]

    def add_raw(self):
        self.db.add_raw(self.creds[0], self.creds[1], self.length)

    def close(self):
        self.db.commit()
        self.db.close()
