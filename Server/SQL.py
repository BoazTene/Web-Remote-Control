import sqlite3


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

    def add_raw(self, user_name, password, client):
        self.c.executemany('''INSERT INTO machines VALUES (?,?,?)''', [(user_name, password, client)])

    def exec(self, command):
        return self.c.execute(command)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def delete(self, user_name):
        self.c.execute("DELETE FROM machines WHERE UserName = '%s'" % user_name)
