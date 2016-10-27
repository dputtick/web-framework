import socket as s
from threading import Thread
from concurrent.futures import ThreadPoolExecutor as Executor


SERVER_ADDRESS = ('localhost', 8080)


class ThreadPoolServer():
    def __init__(self, addr):
        self.addr = addr
        self.executor = Executor()


    def _bind_listening_socket(self):
        self.listening_socket = s.socket()
        self.listening_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.listening_socket.bind(self.addr)
        self.listening_socket.listen(10)


    def run(self):
        print("Serving on: ", self.addr)
        self._bind_listening_socket()
        while True:
            client, addr = self.listening_socket.accept()
            print("Client connected on: ", addr)
            future = self.executor.submit(self._client_connection, client, addr)
            result = future.result()


    def _handle_request(self, request):
        request = request.decode()
        request_list = request.split("\r\n")[0].split(" ")
        request_dict = {'type': request_list[0], 'path': request_list[1]}
        response_header = "HTTP/1.1 200 OK\r\n\r\n"
        return response_header + self._serve_page("Hello")


    def _client_connection(self, client, addr):
        while True:
            request = client.recv(1024)
            if not request:
                break
            page = self._handle_request(request)
            print(page)
            response = str(page).encode() + b'\n'
            client.send(response)
            client.close()
        print("Client connection closed: ", addr)


    def _serve_page(self, page):
        with open("hello.html", 'r') as f:
            return f.read()


def main():
    server = ThreadPoolServer(SERVER_ADDRESS)
    server.run()


if __name__ == '__main__':
    main()
