from Server.SQL import DataBase


# This class update the database if clients disconnect
# s is the socket
# clients is a list of all the clients
# You must first call the start function
class ConnectionCheck:
    def __init__(self, s, clients):
        self.s = s
        self.clients = clients

        self.connect_db()

        self.dead_machine_clients = []
        self.dead_remote_clients = []

    # this class is used to connect to the database and save the data into self.data
    def connect_db(self):
        self.db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db")
        self.data = self.db.get_data()

    # this is the main function
    def start(self):
        self.check_who_alive()

        self.delete_dead_remote_clients()
        self.delete_dead_machines_clients()

        self.save_database_changes()

        return self.clients

    # this function saves the changes
    def save_database_changes(self):
        self.db.commit()
        self.db.close()

    # this function checks each client if he connected
    def check_who_alive(self):
        for row in self.data:
            try:
                self.clients.data[int(row[2])][0].send(b"Alive Check")
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError):
                self.dead_machine_clients.append(row[0])
            except IndexError:
                pass

            try:
                if self.clients.data[int(row[2])][1] is not None:
                    self.clients.data[int(row[2])][1].send(b"Alive Check")
            except ConnectionResetError:
                self.dead_remote_clients.append(int(row[2]))
            except IndexError:
                continue

    # this function delete all the not connected machines
    def delete_dead_machines_clients(self):
        for user_name in self.dead_machine_clients:

            for i in self.db.exec("SELECT * FROM machines WHERE UserName = '%s'" % user_name):
                index = i[2]

                try:
                    self.clients.data.pop(int(index))
                    self.db.delete(user_name)
                    print("Deleted " + user_name)
                except Exception:
                    pass

    # this function delete all the not connected remote clients
    def delete_dead_remote_clients(self):
        for i in self.dead_remote_clients:
            try:
                self.clients.data[i][1] = None
                self.clients.data[i][0].send(b"disconnected")
                print("Delete remote machine")
            except IndexError:
                print("IndexError")
                pass

    # this function checks if the database is not updated
    def check_database_update(self):
        self.connect_db()
        try:
            if len(self.data) != len(self.clients.data):
                self.db.exec("DELETE FROM machines")
                self.db.commit()
                self.db.close()

                self.clients.data = []

                return True
            else:
                return False
        except TypeError:
            return False