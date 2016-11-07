import framework


if __name__ == '__main__':
    app = framework.make_app()
    framework.use_default_server()
    framework.run(ip = 'localhost', port = "8080")
