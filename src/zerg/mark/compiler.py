# -*- coding: utf-8 -*-
import os

from markdown import markdown
from ndict import ndict
from bs4 import BeautifulSoup

from zerg.mark.handlers import Handler
from zerg.settings import jinja_env


class Document:
    def __init__(self, src):
        self.origin = ndict(
            fpath=str(),
            content=src
        )
        self.soup = BeautifulSoup(markdown(src), 'html.parser')

        self.handler = ndict(
            author=str(),
            title=str(),
            hnodes=None
        )

    @property
    def html(self):
        return self.soup.prettify()

    def execute(self, handler):
        handler(self)

    def generate(self):
        template = jinja_env.get_template('template.jinja2')
        html = template.render(document=self)
        return html

    def generate_fp(self, fp):
        fp.write(self.generate())

    def generate_fpath(self, fpath, encoding='utf-8'):
        with open(fpath, 'w', encoding=encoding) as f:
            f.write(self.generate())


class DocumentFp:
    def __new__(cls, fp):
        return Document(fp.read())


class DocumentFpath:
    def __new__(cls, fpath, encoding='utf-8'):
        document = Document(open(fpath, encoding=encoding).read())
        document.origin.fpath = os.path.abspath(fpath)
        return document


if __name__ == '__main__':
    document = DocumentFpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md')
    document.execute(Handler.SetAuthor('Mohanson'))
    document.execute(Handler.SetTitle())
    document.execute(Handler.SetDirectory())
    print(document.soup)
    document.generate_fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.html')