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

def _stop_listen(subscriber,event_type):
    try:
       if subscriber not in _subscribers:
            return "not subscribed before"

       if not _subscribers[subscriber].subscribed(event_type):
            return "not subscribed before"

       _subscribers[subscriber].unsubscribe(event_type)

    finally:
        if not _subscribers[subscriber].has_subscription:
            _subscribers[subscriber].shutdown()
    
    return "unsubscribed"
    


@settings.app.get('/stoplisten/<subscriber:re:[a-zA-Z0-9_\-]+>/<event_type:re:[a-zA-Z0-9_\-]+>')
def stop_listen(subscriber,event_type):
    bottle.response.status=200
    return _stop_listen(subscriber,event_type)
    


@settings.app.get('/listen/<subscriber:re:[a-zA-Z0-9_\-]+>/<event_type:re:[a-zA-Z0-9_\-]+>')
def listen(subscriber,event_type):
    ws = bottle.request.environ.get('wsgi.websocket')
    if subscriber not in _subscribers:
        _subscribers[subscriber] = Subscriber(subscriber)

    subscribed_event_type,subscribed = _subscribers[subscriber].subscribe(event_type)
    event_queue = subscribed_event_type.callback_module.events

    if not _subscribers[subscriber].started:
        _subscribers[subscriber].start()

    while _subscribers[subscriber].subscribed(subscribed_event_type.event_type):
        event = None
        try:
            #print("Wait events for {}->{}".format(subscriber,event_type))
            event = event_queue.get(block=True,timeout=2)
            ws.send(event)
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break
    _stop_listen(subscriber,event_type)

    print("close websocket for {}.{}".format(subscriber,event_type))

