import bottle

import settings

from eventhub_client import Publisher

_publishers = {}
@settings.app.post('/publish')
def publish():
    publisher = bottle.request.POST.get('publisher')
    event_type = bottle.request.POST.get('event_type')
    payload = bottle.request.POST.get('payload')
    if not publisher:
        raise Exception("Missing publisher")

    if not event_type:
        raise Exception("Missing event type")

    if not payload:
        raise Exception("Missing payload")

    key = (publisher,event_type)
    if key not in _publishers:
        _publishers[key] = Publisher(publisher,event_type)

    _publishers[key].publish(payload)

    bottle.response.status=200
    return "ok"


