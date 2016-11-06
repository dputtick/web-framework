'''
This server works
'''

import asyncio


SERVER_ADDRESS = ('localhost', 8080)


async def echo(reader, writer):
    address = writer.get_extra_info('peername')
    print("Connection: ", address)
    while True:
        data = await reader.read(128)
        if data:
            print("Received! ", data)
            writer.write(data)
            await writer.drain()
        else:
            writer.close()
            return


def main():
    event_loop = asyncio.get_event_loop()
    factory = asyncio.start_server(echo, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(factory)
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    event_loop.close()


if __name__ == '__main__':
    main()
