from __future__ import absolute_import

from xml.dom.minidom import parseString

from .settings import crap


class ContentParser(object):
    def __init__(self, raw_document):
        self.document = parseString(raw_document)

    def _remove_crap(self, document):
        for tagname in crap:
            nodes = document.getElementsByTagName(tagname)
            for node in reversed(nodes):
                node.parentNode.removeChild(node)

    def process(self):
        document = self.document
        self._remove_scripts(document)
        print self.document.toxml()
