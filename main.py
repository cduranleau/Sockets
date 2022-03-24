#!/usr/bin/env python3
import sys
import websockets
import asyncio
import os

HOST = os.getenv('SOCKETS_HOST', 'localhost')


def getPort(topic_name, protocal):
    if protocal == "sub":
        return 1234
    return 1235


pubs = []
subs = []


async def new_sub(new_sub):
    subs.append(new_sub)
    print("New subscription. Total number of subs: " +
          str(len(subs)))


async def new_pub(new_pub):
    pubs.append(new_pub)
    print("New publisher. Total number of pubs: " +
          str(len(pubs)))
    async for message in new_pub:
        # Keep watching the subscription for new messages
        for s in subs:
            await s.send(message)


async def createTopic(topic_name):
    async with websockets.serve(new_pub, HOST, getPort(topic_name, "pub")), websockets.serve(new_sub, HOST, getPort(topic_name, "sub")):
        await asyncio.Future()  # run forever


async def sub_topic(topic_name):
    # TODO Client drops connection between messages. This is probably not ideal but is dependent on
    # load and use case. Look into heartbeating to keep connections alive if load testing proves
    # the price of recreating the connection is 'expensive'.
    while True:
        async with websockets.connect("ws://" + HOST + ":" + str(getPort(topic_name, 'sub'))) as s:
            print("+ " + await s.recv())


async def pub_client(topic_name):
    # TODO Client drops connection between messages. This is probably not ideal but is dependent on
    # load and use case. Look into heartbeating to keep connections alive if load testing proves
    # the price of recreating the connection is 'expensive'.
    while True:
        async with websockets.connect("ws://" + HOST + ":" + str(getPort(topic_name, 'pub'))) as s:
            await s.send(input("* "))


def main(mode, topic_name):
    if(mode == 'new_topic'):
        asyncio.run(createTopic(topic_name))
    elif(mode == 'pub_topic'):
        asyncio.run(pub_client(topic_name))
    elif(mode == 'sub_topic'):
        asyncio.run(sub_topic(topic_name))
    else:
        print(
            "Invalid mode. Should be ['new_topic' || 'sub_topic' || 'pub_topic']")


if __name__ == '__main__':
    if(len(sys.argv) < 3):  # Make sure we're given a 'mode' and a 'topic_name'
        main(None, None)
    else:
        main(sys.argv[1], sys.argv[2])
