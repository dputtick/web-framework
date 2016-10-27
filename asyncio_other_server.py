import asyncio
import asyncio.streams as streams


class MyServer:
    def __init__(self):
        self.server = None
        self.clients = {}
        print("Server made")


    def _accept_client(self, client_reader, client_writer):
        task = asyncio.Task(self._handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader, client_writer)

        def client_done(task):
            print("Client task done: ", task)

        task.add_done_callback(client_done)


    @asyncio.coroutine
    def _handle_client(self, client_reader, client_writer):
        while True:
            data = (yield from client_reader.readline()).decode()
            if not data:
                break
            client_writer.write(data)
        yield from client_writer.drain()


    def start(self, loop):
        self.server = loop.run_until_complete(
            streams.start_server(self._accept_client,
                                            '127.0.0.1',
                                            8080,
                                            loop=loop))
        print("Server started")


    def stop(self, loop):
        if self.server is not None:
            self.server.close()
            print("Server stopped")
            loop.run_until_complete(self.server.wait_close())
            self.server = None


def main():
    loop = asyncio.get_event_loop()
    server = MyServer()
    server.start(loop)


if __name__ == '__main__':
    main()
