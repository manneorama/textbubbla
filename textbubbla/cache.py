# -*- coding: utf8 -*-
import memcache
import requests

SERVERS = ['localhost']
TIMEOUT = 600

READABILITY_TOKEN = '854b2903108ad3c485a2b4af41c4009df6cd2cf2'
READABILITY_API = 'http://readability.com/api/content/v1/parser?url={}&token={}'


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


def get_and_save_excerpt(url):
    if not _client().get(url):
        r = requests.get(READABILITY_API.format(url, READABILITY_TOKEN))
        # fucking ugly fucking hack
        # because the fucking excerpt
        # returned by the fucking readability api
        # is unicode encoded as ascii in a unicode
        # container and i fucking don't have the
        # fucking energy to fucking fix it
        try:
            _client().set(url, r.json()['excerpt']
                          .replace(u'&#xE4;', u'ä')
                          .replace(u'&#xE5;', u'å')
                          .replace(u'&#xF6;', u'ö')
                          .replace(u'&hellip;', u'')
                          .replace(u'&#x2013;', u'')
                          .replace(u'&#xC4;', u'Ä')
                          .replace(u'&#xC5;', u'Å')
                          .replace(u'&#xB7;', u'')
                          .replace(u'&#13;', u'') + '...',
                          time=TIMEOUT)
        except:
            _client().set(url, 'Could not generate excerpt :(...')
    return {'excerpt': _client().get(url)}


def get(key):
    return _client().get(str(key))
