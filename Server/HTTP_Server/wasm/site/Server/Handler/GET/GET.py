from Handler.GET.SQL import DataBase
from Handler.GET.GET_Login.GET import GET as GET_Login
from Handler.GET.GET_RemoteControl.GET import GET as remoteControl
from Handler.GET.GET_file.GET import GET as GET_file


class GET:
    def __init__(self, handler, path, root_directory):
        self.handler = handler
        self.path = path
        self.root_directory = root_directory
        try:
            if list(self.path.split("/", 1)[1])[0] == "?" or list(self.path.split("/", 1)[1])[0] == "#":
                access = Access(self.handler)
                if access.check():
                    # remote control the user is authorized
                    remoteControl(handler, path, "../RemoteControl")
                    return
                else:
                    # Login the user is unauthorized
                    GET_Login(handler, path, root_directory)
                    return
            else:
                # its a static file like js, css
                GET_file(handler, path, root_directory)
                return
        except IndexError:
            GET_Login(handler, path, root_directory)
            return


class Access:
    def __init__(self, handler):
        self.address = handler.client_address[0]
        self.path = handler.path
        try:
            self.user_name, self.password = self.get_username_and_password()
        except Exception:
            self.user_name, self.password = None, None

        self.db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db") # Authorized

    def get_username_and_password(self):
        parameters = [parameter.split("=") for parameter in self.path.split("?", 1)[1].split("&")]

        return [parameter[1] for parameter in parameters if parameter[0] == 'username' or parameter[0] == "password"]

    def check(self):
        if self.user_name is None or self.password is None:
            return False

        data = self.db.get_spec_data("address", self.address, "Authorized")

        for row in data:
            if row[1] == self.user_name and row[2] == self.password and row[3] == 0:
                return True

        return False
