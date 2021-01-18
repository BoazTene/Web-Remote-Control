import email.utils
import os
from http import HTTPStatus
import urllib.parse
from .Permission import Permission
from .Path import Path
import shutil


class GET:
    def __init__(self, handler, path, root_directory):
        try:
            self.handler = handler
            self.headers = handler.headers
            self.wfile = handler.wfile
            self.date_time_string = handler.date_time_string

            self.path = Path(path, root_directory=root_directory)

            f = self.send_head(self.path)
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
        except Exception as e:
            print("Error: ", e)

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def send_head(self, path):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """

        permission = Permission(path.remove_parameters())

        if not permission.is_authorized():
            self.send_error(HTTPStatus.FORBIDDEN, "Forbidden", explain="You don't have access to the requested file.")
            self.end_headers()
            return None

        f = None
        if os.path.isdir(path.path) :
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # Sends a forbidden error
                self.send_response(HTTPStatus.FORBIDDEN)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path.path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                self.send_response(HTTPStatus.FORBIDDEN)
                self.end_headers()
                return None
        ctype = path.guess_type()

        # check for trailing "/" which should return 404. See Issue17324
        # The test for this was added in test_httpserver.py
        # However, some OS platforms accept a trailingSlash as a filename
        # See discussion on python-dev and Issue34711 regarding
        # parseing and rejection of filenames with a trailing slash
        if path.path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = open(path.path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            fs = os.fstat(f.fileno())
            # Use browser cache if possible
            if ("If-Modified-Since" in self.headers
                    and "If-None-Match" not in self.headers):
                # compare If-Modified-Since and time of last file modification
                try:
                    ims = email.utils.parsedate_to_datetime(
                        self.headers["If-Modified-Since"])
                except (TypeError, IndexError, OverflowError, ValueError):
                    # ignore ill-formed values
                    pass

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def send_response(self, code, message=None):
        self.handler.send_response(code, message=message)

    def send_header(self, keyword, value):
        self.handler.send_header(keyword, value)

    def send_error(self, code, message=None, explain=None):
        self.handler.send_error(code, message=message, explain=explain)

    def end_headers(self):
        self.handler.end_headers()
