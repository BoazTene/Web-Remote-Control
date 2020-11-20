import sqlite3


# This class is used to handle the database
class DataBase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    # This function return list of all the data in the db
    def get_data(self):
        data = []

        for row in self.c.execute('SELECT * FROM machines'):
            data.append(row)

        return data

    # adds another raw to the table
    def add_raw(self, user_name, password, client):
        self.c.executemany('''INSERT INTO machines VALUES (?,?,?)''', [(user_name, password, client)])

    # let you run any command on the database
    def exec(self, command):
        return self.c.execute(command)

    # commits the changes
    def commit(self):
        self.conn.commit()

    # closes the connection with the database
    def close(self):
        self.conn.close()

    # deletes a raw
    def delete(self, user_name):
        self.c.execute("DELETE FROM machines WHERE UserName = '%s'" % user_name)
