import queue
import bottle

#from bottle.ext.websocket import GeventWebSocketServer
#from bottle.ext.websocket import websocket

import settings

from eventhub_client import Subscriber


_subscribers = {}

@settings.app.get('/')
def index():
    return template('index')

def _stop_listen(subscriber,event_type,client_id):
    key = "{}_{}".format(subscriber,client_id)
    try:
       if key not in _subscribers:
            return "not subscribed before"

       if not _subscribers[key].subscribed(event_type):
            return "not subscribed before"

       _subscribers[key].unsubscribe(event_type)

    finally:
        if not _subscribers[key].has_subscription:
            _subscribers[key].shutdown()
    
    return "unsubscribed"
    


@settings.app.get('/stoplisten/<subscriber:re:[a-zA-Z0-9_\-]+>/<event_type:re:[a-zA-Z0-9_\-]+>/<client_id:re:[0-9]+>')
def stop_listen(subscriber,event_type,client_id):
    bottle.response.status=200
    return _stop_listen(subscriber,event_type,client_id)
    


@settings.app.get('/listen/<subscriber:re:[a-zA-Z0-9_\-]+>/<event_type:re:[a-zA-Z0-9_\-]+>/<client_id:re:[0-9]+>')
def listen(subscriber,event_type,client_id):
    key = "{}_{}".format(subscriber,client_id)
    ws = bottle.request.environ.get('wsgi.websocket')
    if key not in _subscribers:
        _subscribers[key] = Subscriber(subscriber)

    subscribed_event_type,subscribed = _subscribers[key].subscribe(event_type)
    event_queue = subscribed_event_type.callback_module.events

    if not _subscribers[key].started:
        _subscribers[key].start()

    while _subscribers[key].subscribed(subscribed_event_type.event_type):
        event = None
        try:
            #print("Wait events for {}->{}".format(subscriber,event_type))
            event = event_queue.get(block=True,timeout=2)
            ws.send(event)
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break
    _stop_listen(subscriber,event_type,client_id)

    print("close websocket for {}.{}; client_id={}".format(subscriber,event_type,client_id))

