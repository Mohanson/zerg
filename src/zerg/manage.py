# -*- coding: utf-8 -*-
import argparse
import os

from zerg.mark import DocumentFpath, Handler

epilog = """
Sample:
    zerg /home/user/readme.md --author=Mohanson --title=README
"""

parser = argparse.ArgumentParser(description='zerg', prog='zerg', epilog=epilog)
parser.add_argument('src', action='store', type=str, help='src')
parser.add_argument('--author', action='store', type=str, help='author name')
parser.add_argument('--title', action='store', type=str, help='title')


def main():
    args = parser.parse_args()
    document = DocumentFpath(args.src)
    document.execute(Handler.SetAuthor(args.author))
    document.execute(Handler.SetTitle(args.title))
    document.execute(Handler.SetDirectory())
    document.execute(Handler.DrawCode())
    document.generate_fpath(os.path.join(os.path.dirname(document.origin.fpath), document.handler.title + '.html'))


if __name__ == '__main__':
    main()