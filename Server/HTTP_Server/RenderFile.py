
from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase
from typing import Any, Optional


class RenderFile:
    def __init__(self, path):
        self.path = path

        self.data = self.get_file_data()

    def get_file_data(self):
        f = open(self.path, 'r')
        data = f.read()
        f.close

        return data

    def render(self, mime_type):
        return Response(self.data, mimetype=mime_type)


class JSONMixin:
    @property
    def is_json(self) -> bool: ...
    @property
    def json(self): ...
    def get_json(self, force: bool = ..., silent: bool = ..., cache: bool = ...): ...
    def on_json_loading_failed(self, e: Any) -> None: ...


class Response(ResponseBase, JSONMixin):
    default_mimetype: Optional[str] = ...
    @property
    def max_cookie_size(self) -> int: ...