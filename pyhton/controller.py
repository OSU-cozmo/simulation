import server
import state
svr = server.Server()
st = state.worldState()


def sampleInit(body):
    print(body)

svr.bind('INIT', st.initState)

svr.start()
