import bottle 

import settings

from publish import *
from subscribe import *

from eventhub_client import models

from gevent import monkey; 
monkey.patch_all()

@settings.app.route('/static/<path:path>')
def callback(path):
    return bottle.static_file(path,settings.STATIC_ROOT)


@settings.app.get('/')
def index():
    #only list managed subscribed event types
    subscribed_events = models.SubscribedEventType.select().where(
        (models.SubscribedEventType.category==models.TESTING) & 
        (models.SubscribedEventType.event_processing_module.is_null(False))  
    ).order_by(models.SubscribedEventType.publisher,models.SubscribedEventType.event_type,models.SubscribedEventType.subscriber)
    event_tree = []
    for subscribed_event in subscribed_events:
        #only list managed event types
        if not event_tree or event_tree[-1][0] != subscribed_event.publisher:
            event_tree.append((subscribed_event.publisher,[(subscribed_event.event_type,[subscribed_event.subscriber])]))
        elif event_tree[-1][1][-1][0] != subscribed_event.event_type:
            event_tree[-1][1].append((subscribed_event.event_type,[subscribed_event.subscriber]))
        else:
            event_tree[-1][1][-1][1].append(subscribed_event.subscriber)

    return bottle.template('index',debug=settings.DEBUG,port=settings.PORT,event_tree=event_tree)

#run(host='127.0.0.1', port=settings.PORT, server=GeventWebSocketServer)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketServer, WebSocketError

server = WebSocketServer((settings.HOST, settings.PORT), settings.app)
print("Listen to http://{}:{}".format(settings.HOST,settings.PORT))
server.serve_forever()
