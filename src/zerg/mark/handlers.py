# -*- coding: utf-8 -*-
import os

import markdown
from bs4 import BeautifulSoup

from zerg.settings import logger


class Handler:
    empty = object()


class NewHandler(Handler):
    def __init__(self, origin):
        self.origin = origin

    def handle(self, mark):
        mark.set('_origin_content', self.origin)

    class Fp(Handler):
        def __init__(self, fp):
            self.origin = fp.read()

        def handle(self, mark):
            mark.set('_origin_content', self.origin)

    class Fpath(Handler):
        def __init__(self, fpath, encoding='utf-8'):
            basename = os.path.basename(fpath)
            self.name = basename.split('.')[0]

            with open(fpath, 'r', encoding=encoding) as f:
                self.origin = f.read()

        def handle(self, mark):
            mark.set('_origin_content', self.origin)
            mark.set('_filename', self.name)


class InitHandler(Handler):
    def handle(self, mark):
        mark.set('_html', markdown.markdown(mark.get('_origin_content')))
        mark.set('_soup', BeautifulSoup(mark.get('_html'), 'html.parser'))


class TitleHandler(Handler):
    def handle(self, mark):
        if mark.get('_filename'):
            mark.set('_title', mark.get('_filename'))
            return
        first_h = mark.get('_soup').find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if first_h:
            mark.set('_title', str(first_h.string))
            return
        first_p = mark.get('_soup').find('p')
        if first_p:
            mark.set('_title', str(first_p.string[0: 10]))
            return
        mark.set('_title', 'Mark By Zerg')


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
        logger.info('start run HtreeHandler for %s' % mark.get('_title'))
        for index, h in enumerate(mark.get('_soup').find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            hinfo = self.insert_into_hinfos(self.hinfos, h)
            h['id'] = hinfo['id']

        mark.set('_hinfos', self.hinfos)
        mark.set('_html', mark.get('_soup').prettify())


class HtreeFormatHandler(Handler):
    def handle(self, mark):
        for index, h in enumerate(mark.get('_soup').find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            _name = {1: 'h1',
                     2: 'h2',
                     3: 'h3'}.get(h['id'].count('.') + 1)
            h.name = _name

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
                    i['children'] = format_hinfos(i['children'])
            return branch

        mark.set('_hinfos', format_hinfos(mark.get('_hinfos')))
        mark.set('_html', mark.get('_soup').prettify())