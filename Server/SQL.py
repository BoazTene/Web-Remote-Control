import sqlite3


class DataBase:
    """
    This class is used to handle the database
    """

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def get_data(self):
        """
        This function return list of all the data in the db
        :return:
        """

        data = []

        for row in self.c.execute('SELECT * FROM machines'):
            data.append(row)

        return data

    def add_raw(self, user_name, password, client):
        """
        adds another raw to the table
        :param user_name:
        :param password:
        :param client:
        :return:
        """

        self.c.executemany('''INSERT INTO machines VALUES (?,?,?)''', [(user_name, password, client)])

    def exec(self, command):
        """
        let you run any command on the database
        :param command:
        :return:
        """
        return self.c.execute(command)

    def commit(self):
        """
        This function commits the changes
        """
        self.conn.commit()

    def close(self):
        """
        closes the connection with the database
        :return:
        """

        self.conn.close()

    def delete(self, user_name):
        """
        closes the connection with the database
        :param user_name:
        :return:
        """

        self.c.execute("DELETE FROM machines WHERE UserName = '%s'" % user_name)
