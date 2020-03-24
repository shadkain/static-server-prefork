from socket import socket

from pkg.config import Config
from pkg.request import Request
from pkg.response import Response
from pkg.responder import Responder


class Worker(object):
    def __init__(self, sock: socket, conf: Config):
        self.__sock = sock
        self.__conf = conf

        self.__resp = Responder(conf)

    def run(self):
        self.__cycle()
        
    def __cycle(self):
        while True:
            conn, _ = self.__sock.accept()
            conn.settimeout(10)
            self.__handle(conn)

    def __handle(self, conn: socket):
        try:
            raw_request = conn.recv(1024)
            req = Request(raw_request.decode('utf-8'))
            res = self.__resp.make_response(req)
            res.send(conn)
        except:
            pass
        finally:
            conn.close()