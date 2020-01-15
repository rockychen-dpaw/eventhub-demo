from bottle import get, template

import settings

@get('/')
def index():
    return template('index')

@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else:
            break
    users.remove(ws)

