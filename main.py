#!/usr/bin/env python3
import sys
import websockets
import asyncio
import os

PORT = os.getenv('SOCKETS_PORT', 1234)
HOST = os.getenv('SOCKETS_HOST', 'localhost')


async def echo(s):
    async for message in s:
        await s.send(message)  # Echo the message back to the client
        print("+ " + message)  # Write the message to STDIO


async def server():
    async with websockets.serve(echo, HOST, PORT):
        await asyncio.Future()  # run forever


async def client():
    # TODO Client drops connection between messages. This is probably not ideal but is dependent on
    # load and use case. Look into heartbeating to keep connections alive if load testing proves
    # the price of recreating the connection is 'expensive'.
    while True:
        async with websockets.connect("ws://" + HOST + ":" + str(PORT)) as s:
            await s.send(input("* "))
            print("+ " + await s.recv())


def main(mode):
    if(mode == 'server'):
        asyncio.run(server())
    elif(mode == 'client'):
        asyncio.run(client())
    else:
        print("Invalid mode. Should be ['server' || 'client']")


if __name__ == '__main__':
    if(len(sys.argv) < 2):  # Make sure we're given a 'mode'
        main(None)
    else:
        main(sys.argv[1])
