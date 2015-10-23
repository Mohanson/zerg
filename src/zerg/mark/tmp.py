# -*- coding: utf-8 -*-
def execute_draw_codes(self, lexical=None, linenos=False):
        self.is_draw_code = True

        from pygments import highlight
        from pygments.lexers import guess_lexer, get_lexer_by_name
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