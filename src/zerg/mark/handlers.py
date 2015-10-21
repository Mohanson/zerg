# -*- coding: utf-8 -*-
import os

from zerg.settings import logger


class HandlerImp:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class HandlerSetAuthor(HandlerImp):
    def __init__(self, author):
        self.author = author

    def __call__(self, document):
        document.handler.author = self.author


class HandlerSetTitle(HandlerImp):
    def __init__(self, title=''):
        self.title = title

    def __call__(self, document):
        if self.title:
            document.handler.title = self.title if self.title else str()
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
            logger.info('|    ' * (node.deep - 1) + node.id + ' ' + node.string)
            node.show()

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
    def __init__(self, format=True):
        self.format = format

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


class Handler:
    SetAuthor = HandlerSetAuthor
    SetTitle = HandlerSetTitle
    SetDirectory = HandlerSetDirectory