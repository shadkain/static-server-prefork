from urllib import parse

from pkg.log import log


class Request(object):
    def __init__(self, raw: str):
        self.__parse(raw)

    def __parse(self, raw: str):
        parts = raw.split('\r\n')
        try:
            method, url, protocol = parts[0].split(' ')
            url = parse.unquote(url)

            log(f'url: {url}')
            log(f'method: {method}')

            if '?' in url:
                url = url[:url.index('?')]
            
            self.url = url
            self.method = method
            self.protocol = protocol
            
        except Exception:
            pass