# -*- coding: utf-8 -*-
import sys

from zerg.settings import project
from zerg import DocumentFpath, Handler

sys.path.append(project.parent.parent.joinpath('eggs'))

if __name__ == '__main__':
    document = DocumentFpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md')
    document.execute(Handler.SetAuthor('Mohanson'))
    document.execute(Handler.SetTitle())
    document.execute(Handler.SetDirectory())
    document.execute(Handler.DrawCode())
    document.generate_fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.html')