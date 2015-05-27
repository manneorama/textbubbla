# -*- coding: utf8 -*-
import memcache
import requests

SERVERS = ['localhost']
TIMEOUT = 600


def _client():
    return memcache.Client(servers=SERVERS)


def must_repopulate(key):
    if get(key) is None:
        return True
    return False


def populate_from_url(key, url, callback):
    ''' upon completed request, callback is called
    once with request content. callback must return
    a value suitable for insertion into the cache '''
    try:
        content = requests.get(url).content
        value = callback(content)
    except:
        return False

    return _client().set(str(key), value, time=TIMEOUT)


def get(key):
    return _client().get(str(key))
