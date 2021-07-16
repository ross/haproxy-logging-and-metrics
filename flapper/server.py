#!/usr/bin/env python

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket, \
    timeout as Timeout
from threading import Thread
from time import time, sleep
import logging


class BaseHandler(Thread):

    def __init__(self, conn, ip, port):
        super(BaseHandler, self).__init__(name=self.__class__.__name__)
        self.conn = conn
        self.ip = ip
        self.port = port


class EchoHandler(BaseHandler):
    log = logging.getLogger('EchoHandler')

    def run(self):
        self.log.debug('waiting for data')
        data = self.conn.recv(1024)
        if data:
            self.log.debug('reply sent')
            self.conn.sendall(data)
        else:
            self.log.debug('no data recieved no reply')
        self.conn.close()


class FakeHttpHandler(BaseHandler):
    log = logging.getLogger('FakeHttpHandler')

    def run(self):
        self.log.debug('waiting for request')
        data = self.conn.recv(1024)
        self.conn.sendall(b'''HTTP/1.1 200 OK
Content-Type: text/plain

OK
''')
        self.log.debug('response sent')
        self.conn.close()


class TcpServer(Thread):

    def __init__(self, port, handler, cycle_time=30.0, address='0.0.0.0'):
        super(TcpServer, self).__init__(name=f'TcpServer({address}, {port})')
        self.port = port
        self.handler = handler
        self.cycle_time = cycle_time
        self.address = address
        self.timeout = max(cycle_time / 10.0, 1.0)

        self.sock = None

        self.log = logging.getLogger(f'TcpServer({address}, {port})')

    def open(self):
        self.log.info('open:')
        if not self.sock:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.settimeout(self.timeout)
            sock.bind((self.address, self.port))
            sock.listen(1)

            self.sock = sock

    def close(self):
        self.log.info('close:')
        if self.sock:
            self.sock.close()
            self.sock = None

    def toggle(self):
        if self.sock:
            self.close()
        else:
            self.open()

    def run(self):
        start = time()
        while True:
            if self.sock:
                try:
                    (conn, (ip, port)) = self.sock.accept()
                    handler = self.handler(conn, ip, port)
                    handler.start()
                except Timeout:
                    pass
            else:
                sleep(self.timeout)
            now = time()
            if now - start > self.cycle_time:
                self.toggle()
                start = now

logging.basicConfig(level=logging.INFO)

echo = TcpServer(22, EchoHandler, cycle_time=30)
echo.open()
echo.start()
echo = TcpServer(80, FakeHttpHandler, cycle_time=35)
echo.open()
echo.start()
