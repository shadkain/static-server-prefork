from pkg.server import Server
from pkg import log


def main():
    server = Server('config.json')
    server.run()

if __name__ == '__main__':
    main()