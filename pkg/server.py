import os
import socket
from multiprocessing import Process

from pkg.config import Config
from pkg.worker import Worker


class Server(object):
    def __init__(self, config_path: str):
        self.__conf = Config.autodetect(config_path)

    def run(self):
        self.__open_conn()
        self.__spawn_workers()
        print(f'server is running on: http://{self.__conf.host}:{self.__conf.port}')

        self.__run()

    def __open_conn(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.__conf.host, self.__conf.port))
        sock.listen(512)

        self.__sock = sock

    def __spawn_workers(self):
        self.__processes = []

        for i in range(self.__conf.cpu_limit):
            process = Process(
                target=Worker(
                    sock=self.__sock,
                    conf=self.__conf,
                ).run
            )
            self.__processes.append(process)
            process.start()

    def __run(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            for process in self.__processes:
                process.terminate()
            self.__sock.close()
