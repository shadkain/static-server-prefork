from os import path
from enum import IntEnum

from pkg.request import Request
from pkg.response import Response
from pkg.config import Config


METHODS = {"GET", "HEAD"}


class HTTPStatus(IntEnum):
    OK = 200
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405


HTTP_STATUS_MESSAGES = {
    HTTPStatus.OK: 'OK',
    HTTPStatus.Forbidden: 'Forbidden',
    HTTPStatus.NotFound: 'Not Found',
    HTTPStatus.MethodNotAllowed: 'Method Not Allowed'
}


class Responder(object):
    def __init__(self, conf: Config):
        self.__conf = conf

    def make_response(self, req: Request) -> Response:
        if req.method not in METHODS:
            return Response(status=HTTPStatus.MethodNotAllowed) 

        if '/../' in req.url:
            return Response(status=HTTPStatus.Forbidden)

        filepath = path.join(self.__conf.root, req.url.lstrip('/'))
        if path.isdir(filepath):
            filepath = path.join(filepath, 'index.html')
            if not path.exists(filepath):
                return Response(status=HTTPStatus.Forbidden)

        if not path.isfile(filepath):
            return Response(status=HTTPStatus.NotFound)

        return Response(status=HTTPStatus.OK, method=req.method, protocol=req.protocol, filepath=filepath)
        