import asyncio
import websockets
import json
import logging;
class server:

    outBuf = []
    stop = False
    lastMsg = 0
    routes = {}
    log = -1
    def __init__(self):
        """Initializes an instance of the robot object."""

        logger = logging.getLogger('SVR')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        #Logs look like
        #Robot > ERROR >> This is and Error
        formatter = logging.Formatter('%(name)s > %(levelname)s >> %(message)s')
        #using tab to line up all messages

        ch.setFormatter(formatter)

        logger.addHandler(ch)
        self.log = logger

    def start(self):
        self.log("Server starting\n")
        self.log.info("Currently Bound Types -> %s" % list(map(lambda x : x, self.routes)))
        _server = websockets.serve(self.handler, 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(_server)
        asyncio.get_event_loop().run_forever()

    async def router(self, msg):

        if "JSON" not in msg:
            self.log.warning("Recieved bad message : %s" % msg)
        else:
            msg = msg.replace("JSON", "")
            nmsg = self.msgToDict(msg)
            if not nmsg:
                self.log.error("Recieved Bad JSON : %s" % msg)
                stopClean()
            else:
                t = nmsg['header']['type'];
                self.log.info("Client Message : '%s'" % nmsg['header']['msg'])
                if t in self.routes:
                    f = self.routes[t](nmsg['body'])
                else:
                    self.log.error("No behavior defined for type %s" % t)
                    stopClean()



    def msgToDict(self, msg):
        try:
            nmsg = json.loads(msg)
        except json.JSONDecodeError as e:
            return False
        return json.loads(msg)

    def bind(self, key, behavior):
        self.routes[key] = behavior

    async def incoming(self, websocket, path):
        async for msg in websocket:
            await self.router(msg.decode("utf-8"))

    async def outgoing(self, websocket, path):
        msg = "hello"
        self.log.info("Outgoing : '%s'" % msg)
        await websocket.send(msg)

    async def handler(self, websocket, path):
        self.log.info("connected to new client");

        inTask = asyncio.ensure_future(self.incoming(websocket, path))
        outTask = asyncio.ensure_future(self.outgoing(websocket, path))
        while True:
            done, pending = await asyncio.wait(
                [inTask, outTask],
                return_when=asyncio.ALL_COMPLETED,
            )

svr = server()

def stopClean(body = None):
    asyncio.get_event_loop().stop()
    asyncio.get_event_loop().close()

def sampleInit(body):
    print("Initializing World State")

svr.bind('STOP', stopClean)
svr.bind('INIT', sampleInit)

svr.start()
