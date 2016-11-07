SERVER = None
DEBUG = False
ROUTES = {}
CACHED_ROUTES = {}

## setup stuff

def make_app():
    # compile all of the routes here
    pass


def choose_server(servername = ""):
    return default_server()


def use_default_server():
    try:
        from server import server
        SERVER = server
    except ImportError:
        raise RuntimeError
    return threadpool_server

## handling stuff

def request_handler(environ, start_response)
    pass


def response_generator()
    pass


def run(ip='localhost', port='8080'):
    address = (ip, port)
    if not SERVER:
        use_default_server()
    server = SERVER
    server.run(request_handler, address)
