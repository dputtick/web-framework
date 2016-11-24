from server import server


def test_make_server():
    server = make_server()
    print(type(server))


def make_server():
    return server.ThreadPoolServer('localhost')
