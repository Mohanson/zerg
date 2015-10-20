# -*- coding: utf-8 -*-
import os

from zerg.settings import logger, jinja_env


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


class HtreeHandler(HandlerImp):
    def __init__(self, rdeep=3):
        self.rdeep = rdeep
        self.hinfos = []

    def insert_into_hinfos(self, branch, h):
        deep, ids = 1, []
        hinfo = {
            'name': str(h.name),
            'string': str(h.string),
            'children': [],
            'id': None,
            'deep': None
        }
        if not (branch and hinfo['name'] > branch[-1]['name'] and deep < self.rdeep):
            ids.append(len(branch) + 1)
            hinfo['id'] = '.'.join([str(i) for i in ids])
            hinfo['deep'] = deep
            branch.append(hinfo)
            logger.info('|    ' * (deep - 1) + hinfo['id'] + ' ' + hinfo['string'])
            return hinfo
        else:
            ids.append(len(branch))
            branch = branch[-1]['children']
            deep += 1
            self.insert_into_hinfos(branch, h)

    def __call__(self, mark):
        logger.info('start run HtreeHandler for %s' % mark.process.title)
        for index, h in enumerate(mark.process.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            hinfo = self.insert_into_hinfos(self.hinfos, h)
            h['id'] = hinfo['id']

        mark.process.hinfos = self.hinfos


class HtreeFormatHandler(HandlerImp):
    @staticmethod
    def format_hinfos(branch):
        for i in branch:
            i['name'] = {
                1: 'h1',
                2: 'h2',
                3: 'h3',
                4: 'h4',
                5: 'h5',
                6: 'h6'
            }.get(i['id'].count('.') + 1)
            if i['children']:
                i['children'] = HtreeFormatHandler.format_hinfos(i['children'])
        return branch

    def handle(self, mark):
        for index, h in enumerate(mark.process.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            _name = {1: 'h1',
                     2: 'h2',
                     3: 'h3'}.get(h['id'].count('.') + 1)
            h.name = _name

        mark.process.hinfos = HtreeFormatHandler.format_hinfos(mark.process.hinfos)


class GenerateHandler(HandlerImp):
    class Fp(HandlerImp):
        def __init__(self, fp):
            self.fp = fp

        def handle(self, mark):
            template = jinja_env.get_template('template.jinja2')
            html = template.render(mark=mark)
            self.fp.write(html)

    class Fpath(HandlerImp):
        def __init__(self, fpath, encoding='utf-8'):
            self.fpath = fpath
            self.encoding = encoding

        def handle(self, mark):
            template = jinja_env.get_template('template.jinja2')
            html = template.render(mark=mark)
            with open(self.fpath, 'w', encoding=self.encoding) as f:
                f.write(html)


class Handler:
    SetAuthor = HandlerSetAuthor
    SetTitle = HandlerSetTitle