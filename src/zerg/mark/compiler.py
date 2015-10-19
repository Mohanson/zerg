# -*- coding: utf-8 -*-

from saika.utils import Paramscheck, Accept

from zerg.settings import RECUR_DEEP, jinja_env
from zerg.mark.handlers import *


class Mark:
    __slot__ = ['_filename', '_origin_content', '_html', '_soup', '_title', '_hinfos']

    def get(self, attr):
        if attr in Mark.__slot__:
            try:
                value = self.__dict__[attr]
            except KeyError:
                value = None
            return value
        else:
            raise KeyError(attr)

    def set(self, key, value):
        if key in Mark.__slot__:
            self.__dict__[key] = value
        else:
            raise KeyError(key)

    def as_dict(self):
        return dict(zip(self.__slot__, map(self.get, self.__slot__)))

    def handle(self, handler):
        handler.handle(self)
        return self


class MarkDown:
    def __init__(self, origin, title=None):

        self._origin = origin
        self._html = markdown.markdown(self._origin)

        self._soup = BeautifulSoup(self._html, 'html.parser')
        # assignment after do_analysis_hinfos()
        self._hinfos = list()
        # document title
        if title:
            self.title = title
        else:
            first_h = self._soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if first_h:
                self.title = str(first_h.string)
            else:
                logger.warning('This document has no title!')
                self.title = 'undefined'

        self.is_draw_code = False  # if True, assert code.css into template.jinja2

    @classmethod
    def from_source(cls, text):
        return MarkDown(origin=text)

    @classmethod
    def from_fp(cls, fp):
        text = fp.read()
        return MarkDown(origin=text)

    @classmethod
    def from_fpath(cls, fpath, encoding='utf-8'):
        name_md = os.path.basename(fpath)
        name = name_md.split('.')[0]

        with open(fpath, 'r', encoding=encoding) as f:
            text = f.read()
        markup = MarkDown(origin=text, title=name)
        return markup

    def _generate(self, title, content, hinfos, is_draw_code):
        template = jinja_env.get_template('template.jinja2')
        return template.render(title=title, content=content, hinfos=hinfos, is_draw_code=is_draw_code)

    def generate(self):
        return self._generate(self.title, self.html, self._hinfos, self.is_draw_code)

    def generate_fp(self, fp):
        r = self.generate()
        fp.write(r)
        return r

    def generate_fpath(self, fpath, encoding='utf-8'):
        with open(fpath, 'w', encoding=encoding) as f:
            return self.generate_fp(f)

    @property
    def html(self):
        return self._soup.prettify()

    @property
    def default_file_name(self):
        return self.title + '.html'

    @Paramscheck(recur=Accept.Lambda('_ in [2, 3]'))
    def execute_analysis_hinfos(self, recur=RECUR_DEEP, format=True):
        """ Structure Analysis of documentation for the title.

        :param recur: deepest level titles(default is 3).
        :param format: default is True. if true, the first level titles will change to <h1>, second level title
            will change to <h2>, e.t.
        :return: self
        """
        logger.info('Do analysis hinfos for %s' % self.default_file_name)
        hset = set()
        for index, h in enumerate(self._soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            hset.add(str(h.name))
            hinfo = {
                'name': str(h.name),
                'string': str(h.string),
                'children': [],
                'id': None,
                'deep': None
            }
            current = self._hinfos
            loop = 1
            id = []
            while current and hinfo['name'] > current[-1]['name'] and loop < recur:
                id.append(len(current))
                current = current[-1]['children']
                loop += 1
            else:
                id.append(len(current) + 1)
                if format:
                    _name = {1: 'h1',
                             2: 'h2',
                             3: 'h3'}.get(len(id))
                    h.name = _name
                # set an anchor point in soup
                h['id'] = hinfo['id'] = '.'.join([str(i) for i in id])
                current.append(hinfo)
            logger.info('|    ' * (loop - 1) + hinfo['id'] + ' ' + hinfo['string'])
        if len(hset) > recur:
            logger.warning('list of nested are too deeply, reset on %s' % recur)
        if format:
            def format_hinfos(current):
                for i in current:
                    i['name'] = {
                        1: 'h1',
                        2: 'h2',
                        3: 'h3',
                        4: 'h4',
                        5: 'h5',
                        6: 'h6'
                    }.get(len(i['id'].split('.')))
                    if i['children']:
                        i['children'] = format_hinfos(i['children'])
                return current

            self._hinfos = format_hinfos(self._hinfos)

    def execute_draw_codes(self, lexical=None, linenos=False):
        self.is_draw_code = True

        from pygments import highlight
        from pygments.lexers import guess_lexer
        from pygments.formatters.html import HtmlFormatter
        from pygments.util import ClassNotFound

        # code = 'print("Hello World")\nresponse = requests.get()'
        # after_draw_code = highlight(code, get_lexer_by_name("py", stripall=True),
        # HtmlFormatter(linenos=False, cssclass="source"))
        # print(after_draw_code)

        # print(HtmlFormatter().get_style_defs('.source'))
        # print(HtmlFormatter().get_style_defs('.sourcetable'))

        for index, pre in enumerate(self._soup.select('pre')):
            code_content = str(pre.string)
            try:
                lexer = guess_lexer(code_content)
            except ClassNotFound:
                logger.info('code block %s colored by %s' % (index, 'Normal String'))
            else:
                after_draw_code_content = highlight(code_content, lexer,
                                                    HtmlFormatter(linenos=linenos, cssclass='source'))
                after_draw_code_content_tag = BeautifulSoup(after_draw_code_content, 'html.parser')
                pre.replace_with(after_draw_code_content_tag)
                logger.info('code block %s colored by %s' % (index, lexer.name))


if __name__ == '__main__':
    r = Mark()
    r.handle(NewHandler.Fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md', 'utf-8'))
    r.handle(InitHandler())
    r.handle(TitleHandler())
    r.handle(HtreeHandler())
    r.handle(HtreeFormatHandler())
