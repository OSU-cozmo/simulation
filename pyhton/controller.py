import server
import state
import asyncio
import json

svr = server.Server()
st = state.worldState()

def getNextCommand(body = None):
    command = {
        "type" : "CMD",
        "msg" : "Next command",
        "seq" : 0,

        "command" : "driveForward",
        "ready" : True
    }

    str = json.dumps(command)
    svr.sendMsg(str, command['msg'])

def initCon(body = None):
    st.initState(body)
    res = {
        "type" : "INIT_S",
        "msg" : "Initialization successful",
        "seq" : 0,

        "ready" : True,
        "command" : "NONE"
    }
    str = json.dumps(res)
    svr.sendMsg(str, res['msg'])

svr.bind('INIT', initCon)
svr.bind('NEXT', getNextCommand)
svr.start()
