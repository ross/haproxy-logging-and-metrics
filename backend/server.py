#!/usr/bin/env python

from random import random
from tornado.gen import sleep
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler


class MainHandler(RequestHandler):

    async def get(self):

        port = self.request.connection.stream.socket.getsockname()[1]

        if port == 81:
            self.set_status(503)
            self.write('Requested Error\n')
            return

        # delays
        if 1000 < port and port < 6000:
            delay = port / 10000.0
            await sleep(delay)

        # errors
        if 11000 < port and port < 20000:
            reliability = (int(port / 1000) - 10) / 10.0
            if reliability > random():
                self.set_status(503)
                self.write('Unlucky Error\n')
                return

        self.write(f'Hello, world!\n')


if __name__ == "__main__":
    app = Application([
        (r"/", MainHandler),
    ])

    # normal
    app.listen(80)

    # always fails
    app.listen(81)

    # delays
    for i in range(1080, 5081, 1000):
        print(f'binding {i}')
        app.listen(i)

    for i in range(11080, 19081, 1000):
        print(f'binding {i}')
        app.listen(i)

    IOLoop.current().start()
