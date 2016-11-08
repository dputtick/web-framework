'''
This was originally threadpool_server.py
'''

import socket as s
from concurrent.futures import ThreadPoolExecutor as Executor
from urllib.parse import parse_qs, urlparse
from http import HTTPStatus


# Constants
DEBUG = True
SERVER_NAME = "Server v. 0.1"


class ThreadPoolServer():
    def __init__(self, addr):
        self.addr = addr
        self.executor = Executor()

    def _create_listening_socket(self):
        self.listening_socket = s.socket()
        self.listening_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.listening_socket.bind(self.addr)
        self.listening_socket.listen(10)

    def _handle_request(self, request):
        environ = self._make_environ(request)
        start_response = self._start_response
        result = self.app(environ, start_response)
        return result

    def _client_connection(self, client, addr):
        while True:
            request = client.recv(1024)
            if not request:
                break
            response = self._handle_request(request)
            response = str(response).encode('utf-8') + b'\n'
            client.send(response)
            client.close()
        if DEBUG:
            print("Client connection closed: ", addr)

    def _make_environ(self, request):
        request = request.decode('utf-8')
        environ = {}
        environ['REQUEST_METHOD'] = None
        return environ

    def _write_data(self, data):
        # this is a callable that should write data if needed (as per WSGI)
        pass

    def _start_response(self, status, response_headers, exc_info=None):
        response_header = "HTTP/1.1 200 OK\r\n\r\n"
        return self._write_data

    def serve(self, app):
        self.app = app
        if DEBUG:
            print("Serving <appname> on: ", self.addr)
        self._create_listening_socket()
        while True:
            client, addr = self.listening_socket.accept()
            if DEBUG:
                print("Client connected on: ", addr)
            fut = self.executor.submit(self._client_connection, client, addr)
            result = fut.result()  # do I need this line? try deleting


def run(app, address):
    server = ThreadPoolServer(address)
    server.serve(app)
