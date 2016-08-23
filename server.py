import socket
import asyncio


SERVER_ADDRESS = ('localhost', 8080)


class Server(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        print(self.address)


    def data_received(self, data):
        self.data = data
        print(data)


    def connect_lost(self, error):
        if error:
            print("Error: ", error)
        else:
            print("Connection lost")
        super().connection_lost(error)


def main():
    event_loop = asyncio.get_event_loop()
    factory = event_loop.create_server(Server, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(factory)
    while True:
        event_loop.run_forever()
        break
    event_loop.close()


if __name__ == '__main__':
    main()

#server received connection from ('127.0.0.1', 61870)
#request we received: b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7\r\nAccept-Language: en-us\r\nDNT: 1\r\nConnection: keep-alive\r\n\r\n'