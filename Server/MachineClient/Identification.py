from Server.SQL import DataBase


class Identification:
    """
    This class checking if the username and password are already in the database.
    """

    DATABASE_PATH = r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db"

    def __init__(self, creds, length):
        self.creds = creds
        self.db = DataBase(self.DATABASE_PATH)

        self.data = self.db.get_data()

        self.length = length

    def check(self):
        """
        This function checks if the creds fit to one of the raw in database
        :return:
        """

        for raw in self.data:
            if self.creds[0] == raw[0]:
                return False

        self.add_raw()
        self.close()
        return True

    def check_remote_client(self):
        """
            This function checks if the creds fit to one of the raw in database
            and returns the number of the raw.
        :return:
        """

        index = 0
        for raw in self.data:
            if self.creds[0] == raw[0] and self.creds[1] == raw[1]:
                return [True, index]
            index += 1

        self.close()
        return [False, None]

    def add_raw(self):
        """
        This function adds raw to the database
        :return:
        """

        self.db.add_raw(self.creds[0], self.creds[1], self.length)

    def close(self):
        """
        This function commits any changes to the database and then close the connection.
        :return:
        """

        self.db.commit()
        self.db.close()
