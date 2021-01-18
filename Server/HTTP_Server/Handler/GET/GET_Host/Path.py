import mimetypes
import os
import urllib.parse
import posixpath


class Path:
    def __init__(self, path, root_directory=""):
        self.extensions_map = mimetypes.types_map.copy()
        self.extensions_map.update({
            '': 'application/octet-stream',  # Default
            '.py': 'text/plain',
            '.c': 'text/plain',
            '.h': 'text/plain',
        })


        self.path = path
        self.root_directory = root_directory #"../Login"

        self.root_dir()

        if self.path.split("/")[1] == "node_modules":
            self.path = "../" + self.path
            self.path = self.translate_path(self.path)
        else:
            self.path = os.path.relpath(self.root_directory + self.path)
            self.path = self.translate_path(self.path)

    def root_dir(self):
        if str(self.remove_parameters()) == '/Host':
            try:
                self.path = '/Host/index.html?' +  self.path.split("?", 1)[1]
            except IndexError:
                self.path = '/Host/index.html'


    def remove_parameters(self):
        return self.path.split("?", 1)[0].split("#", 1)[0]

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]

        path = self.slash_to_back_slash(path)

        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')

        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)

        path = posixpath.normpath(path)

        words = path.split('/')
        words = filter(None, words)

        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)

        if trailing_slash:
            path += '/'
        return path


    def slash_to_back_slash(self, string):
        """ the function gets a string and replace the slashes with back slashes
        :param string:
        :return:
        """
        if len(string.split('/')) > 1:
            return "\\".join(("\\".join(string.split('/'))).split("\\\\"))
        else:
            return string

    def guess_type(self):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        path = os.path.relpath(self.path)

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']