import asyncio
import websockets

class server:

    outBuf = []
    stop = False
    def __init__(self):
        pass;

    def start(self):
        _server = websockets.serve(self.handler, 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(_server)
        asyncio.get_event_loop().run_forever()


    async def router(self, msg):
        print (" > %s" % msg)
        if(msg == "stop"):
            print("Trying to stop")
            asyncio.get_event_loop().stop()
            asyncio.get_event_loop().close();

    async def incoming(self, websocket, path):
        async for msg in websocket:
            await self.router(msg.decode("utf-8"))

    async def outgoing(self, websocket, path):
        print("Sending message")
        await websocket.send("Hello")

    async def handler(self, websocket, path):
        print("connected to %s" % path);

        inTask = asyncio.ensure_future(self.incoming(websocket, path))
        outTask = asyncio.ensure_future(self.outgoing(websocket, path))
        while True:
            done, pending = await asyncio.wait(
                [inTask, outTask],
                return_when=asyncio.ALL_COMPLETED,
            )

svr = server()
svr.start()
