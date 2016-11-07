SERVER = None
DEBUG = False
ROUTES = {}
CACHED_ROUTES = {}

# setup stuff


def make_app():
    # compile all of the routes here
    pass


def choose_server(servername=""):
    return use_default_server()


def use_default_server():
    try:
        from server import server
        global SERVER
        SERVER = server
    except ImportError:
        raise RuntimeError

# handling stuff


def request_handler(environ, start_response):
    # decode the environ and figure out what we need
    response = response_generator()
    return [response]


def response_generator():
    return None


def run(ip='localhost', port='8080'):
    address = (ip, port)
    if not SERVER:
        use_default_server()
    server = SERVER
    server.run(request_handler, address)
