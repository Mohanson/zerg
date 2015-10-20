# -*- coding: utf-8 -*-

from ndict import ndict

from zerg.mark.handlers import *


class Document:
    def __init__(self):
        self.origin = ndict(
            path=None,
            content=None
        )
        self.process = ndict(
            title=None,
            hinfos=[],
            soup=None
        )
        self.result = ndict(
            drawing=False,
        )

    @property
    def html(self):
        return self.process.soup.prettify()

    def handle(self, handler):
        handler.handle(self)
        return self


if __name__ == '__main__':
    r = Document()
    r.handle(NewHandler.Fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md', 'utf-8'))
    r.handle(InitHandler())
    r.handle(TitleHandler())
    r.handle(HtreeHandler())
    r.handle(HtreeFormatHandler())
    r.handle(GenerateHandler.Fpath(r'd:/1.html'))
    print(r.process.soup)
    # print(r.get('_soup'))
