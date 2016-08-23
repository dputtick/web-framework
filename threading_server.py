import socket as s
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool


SERVER_ADDRESS = ('localhost', 8080)


class ProcessPoolServer():
    def __init__(self, addr):
        self.addr = addr
        self._make_process_pool()

    def _bind_listening_socket(self):
        self.listening_socket = s.socket()
        self.listening_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.listening_socket.bind(self.addr)
        self.listening_socket.listen(10)

    def _make_process_pool(self):
        self.pool = Pool(2)

    def run(self):
        print("Serving on: ", self.addr)
        self._bind_listening_socket()
        while True:
            client, addr = self.listening_socket.accept()
            print("Client connected on: ", addr)
            new_thread = Thread(target=self._client_connection, args=(client, addr))
            new_thread.start()

    def _client_connection(self, client, addr):
        while True:
            request = client.recv(100)
            if not request:
                break
            #request = request.decode()
            request = int(request)
            #future = self.pool.submit(self._serve, request)
            #result = future.result()
            result = self._serve(request)
            response = str(result).encode() + b'\n'
            client.send(response)
        print("Client connection closed: ", addr)

    def _serve(self, request):
        return request


def main():
    server = ProcessPoolServer(SERVER_ADDRESS)
    server.run()


if __name__ == '__main__':
    main()