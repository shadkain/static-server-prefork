import os
import mimetypes
from datetime import datetime
from socket import socket

from pkg.log import log


class Response(object):
    def __init__(self, status: int, method: str = 'GET', protocol: str = 'HTTP/1.1', filepath: str = None):
        self.status = status
        self.method = method
        self.protocol = protocol
        self.set_base_headers()
        self.filepath = filepath
        if filepath is not None:
            self.set_mime_headers()

    def set_base_headers(self):
        self.headers = {
            'Connection': 'close',
            'Server': 'python-static-server',
            'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
    
    def set_mime_headers(self):
        mime, _ = mimetypes.guess_type(self.filepath)
        self.headers['Content-Type'] = mime
        self.headers['Content-Length'] = os.path.getsize(self.filepath)

    def send(self, conn: socket):
        hdrs = self.form_headers()
        conn.sendall(hdrs)
        if self.filepath is None or self.method == 'HEAD':
            return

        with open(self.filepath, 'rb') as file:
            conn.sendfile(file)

    def form_headers(self) -> str:
        from pkg.responder import HTTP_STATUS_MESSAGES
        hdrs = f'{self.protocol} {self.status} {HTTP_STATUS_MESSAGES[self.status]}\r\n'
        hdrs += '\r\n'.join([f'{key}: {value}' for key, value in self.headers.items()]) + '\r\n\r\n'
        log(hdrs)
        return hdrs.encode('utf-8')