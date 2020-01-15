from bottle import run
from bottle import get, template

import settings

from subscribe import *

from eventhub_client import models

@get('/')
def index():
    #only list managed subscribed event types
    subscribed_events = models.SubscribedEventType.select().where(models.SubscribedEventType.managed==True).order_by(models.SubscribedEventType.publisher,models.SubscribedEventType.event_type,models.SubscribedEventType.subscriber)
    event_tree = []
    for subscribed_event in subscribed_events:
        #only list managed event types
        if not subscribed_event.event_type.managed:
            continue
        if not event_tree or event_tree[-1][0] != subscribed_event.publisher:
            event_tree.append((subscribed_event.publisher,[(subscribed_event.event_type,[subscribed_event.subscriber])]))
        elif event_tree[-1][1][-1][0] != event.event_type:
            event_tree[-1][1].append((subscribed_event.event_type,[subscribed_event.subscriber]))
        else:
            event_tree[-1][1][-1][1].append(subscribed_event.subscriber)

    return template('index',debug=settings.DEBUG,port=settings.PORT,event_tree=event_tree)

run(host='127.0.0.1', port=settings.PORT, server=GeventWebSocketServer)
