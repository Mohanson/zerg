# -*- coding: utf-8 -*-
import markdown
from bs4 import BeautifulSoup


class MetaHandler(type):
    def __new__(mcs, name, bases, dct):
        dct['handle'] = lambda _: 'World'
        return super(MetaHandler, mcs).__new__(mcs, name, bases, dct)


class I(metaclass=MetaHandler):
    def handle(self):
        return 'Hello'


print(I().handle())


class Handler:
    empty = object()
    require = empty

    def __init__(self):
        self.successor = Handler.empty

    def is_has_successor(self):
        if self.successor != Handler.empty:
            return True
        else:
            return False

    def successor(self, successor):
        self.successor = successor


"""
class InitHandler(Handler):
    def handle(self, mark):
        mark.set('_html', markdown.markdown(mark.get('_origin_content')))
        mark.set('_soup', BeautifulSoup(mark.get('_html'), 'html.parser'))
"""

"""
class TitleHandler(Handler):
    def handle(self, mark):
        if mark.info['_FILE_NAME']:
            mark.info['_TITLE'] = mark.info['_FILE_NAME']
        else:
            first_h = self._soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if first_h:
                self.title = str(first_h.string)
            else:
                logger.warning('This document has no title!')
                self.title = 'undefined'
"""