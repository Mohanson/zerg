# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters.html import HtmlFormatter
from pygments.util import ClassNotFound

from zerg.settings import LOGGER


class HandlerImp:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class HandlerSetAuthor(HandlerImp):
    def __init__(self, author):
        self.author = author

    def __call__(self, document):
        document.handler.author = self.author


class HandlerSetTitle(HandlerImp):
    def __init__(self, caption=None):
        self.caption = caption

    def __call__(self, document):
        if self.caption:
            document.handler.title = self.caption if self.caption else str()
        elif document.origin.fpath:
            name = os.path.basename(document.origin.fpath).split('.')[0]
            document.handler.title = name
        else:
            htag = document.soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if htag:
                document.handler.title = str(htag.string)
            else:
                ptag = document.soup.find('p')
                if ptag:
                    document.handler.title = str(ptag.string)[0:10]
                else:
                    document.handler.title = 'zerg document'


class _HNode:
    def __init__(self, name, string):
        self.name = name
        self.string = string

        self.children = []

        self.parent = None
        self.ids = []

    @property
    def deep(self):
        return len(self.ids)

    @property
    def id(self):
        return '.'.join(list(map(str, self.ids))) or None

    def __str__(self):
        return '_HNode<id=%s, name=%s, string=%s, deep=%s, children=%s>' % (
            self.id, self.name, self.string, self.deep, self.children,
        )

    def __repr__(self):
        return self.__str__()

    def show(self):
        for node in self.children:
            LOGGER.info('|    ' * (node.deep - 1) + node.id + ' ' + node.string)
            node.show()

    def html(self):
        pass

    def insert(self, hnode):
        if not self.children or hnode.deep >= 2:
            hnode.parent = self
            hnode.ids.append(len(self.children) + 1)
            self.children.append(hnode)
        else:
            if self.children[-1].name >= hnode.name:
                hnode.parent = self
                hnode.ids.append(len(self.children) + 1)
                self.children.append(hnode)
            else:
                hnode.ids.append(len(self.children))
                self.children[-1].insert(hnode)
        return hnode


class HandlerSetDirectory(HandlerImp):
    def __init__(self, format=True, show_directory_number=True):
        self.format = format
        self.show_directory_number = show_directory_number

    def __call__(self, document):
        root = _HNode(None, None)
        for index, h in enumerate(document.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            hnode = root.insert(_HNode(str(h.name), str(h.string)))
            h['id'] = hnode.id
            if self.format:
                h.name = {
                    1: 'h1',
                    2: 'h2',
                    3: 'h3'
                }.get(hnode.deep)
        root.show()
        document.handler.hnodes = root
        document.settings.show_directory_number = self.show_directory_number


class HandlerDrawCode(HandlerImp):
    def __init__(self, syntax=None, linenos=True):
        self.sybtax = syntax
        self.linenos = linenos

    def __call__(self, document):
        for index, pre in enumerate(document.soup.select('pre')):
            context = str(pre.string)
            try:
                lexer = guess_lexer(context)
            except ClassNotFound:
                LOGGER.info('code block %s colored by %s' % (index, 'Normal String'))
            else:
                context_drawed = highlight(context, lexer, HtmlFormatter(linenos=self.linenos, cssclass='source'))
                context_soup = BeautifulSoup(context_drawed, 'html.parser')
                pre.replace_with(context_soup)
                LOGGER.info('code block %s colored by %s' % (index, lexer.name))
        document.settings.drawcode = True


class Handler:
    SetAuthor = HandlerSetAuthor
    SetTitle = HandlerSetTitle
    SetDirectory = HandlerSetDirectory
    DrawCode = HandlerDrawCode