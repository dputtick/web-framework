SERVER = None




def choose_server(servername = ""):
    return default_server()


def use_default_server():
    try:
        from server import server
        SERVER = server
    except ImportError:
        raise RuntimeError
    return threadpool_server


def run(ip='localhost', port='8080'):
    address = (ip, port)
    if not SERVER:
        use_default_server()
    server = SERVER
    app = make_app()
    server.serve(app, address)
