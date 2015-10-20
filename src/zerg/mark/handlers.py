# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup
from markdown import markdown

from zerg.settings import logger, jinja_env


class Handler:
    empty = object()


class NewHandler(Handler):
    def __init__(self, content):
        self.content = content

    def handle(self, mark):
        mark.origin.content = self.content

    class Fp(Handler):
        def __init__(self, fp):
            self.content = fp.read()

        def handle(self, mark):
            mark.origin.content = self.content

    class Fpath(Handler):
        def __init__(self, fpath, encoding='utf-8'):
            self.fpath = os.path.abspath(fpath)

            with open(fpath, 'r', encoding=encoding) as f:
                self.content = f.read()

        def handle(self, mark):
            mark.origin.path = self.fpath
            mark.origin.content = self.content


class InitHandler(Handler):
    def handle(self, mark):
        mark.process.soup = BeautifulSoup(markdown(mark.origin.content), 'html.parser')


class TitleHandler(Handler):
    def __init__(self, title=None):
        self.title = title

    def handle(self, mark):
        if self.title:
            mark.process.title = self.title
            return
        if mark.origin.path:
            name = os.path.basename(mark.origin.path).split('.')[0]
            mark.process.title = name
            return
        first_h = mark.get('_soup').find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if first_h:
            mark.process.title = str(first_h.string)
            return
        first_p = mark.get('_soup').find('p')
        if first_p:
            mark.process.title = str(first_p.string[0: 10])
            return
        mark.process.title = 'Mark By Zerg'


class HtreeHandler(Handler):
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

    def handle(self, mark):
        logger.info('start run HtreeHandler for %s' % mark.process.title)
        for index, h in enumerate(mark.process.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            hinfo = self.insert_into_hinfos(self.hinfos, h)
            h['id'] = hinfo['id']

        mark.process.hinfos = self.hinfos


class HtreeFormatHandler(Handler):
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


class GenerateHandler(Handler):
    class Fp(Handler):
        def __init__(self, fp):
            self.fp = fp

        def handle(self, mark):
            template = jinja_env.get_template('template.jinja2')
            html = template.render(mark=mark)
            self.fp.write(html)

    class Fpath(Handler):
        def __init__(self, fpath, encoding='utf-8'):
            self.fpath = fpath
            self.encoding = encoding

        def handle(self, mark):
            template = jinja_env.get_template('template.jinja2')
            html = template.render(mark=mark)
            with open(self.fpath, 'w', encoding=self.encoding) as f:
                f.write(html)