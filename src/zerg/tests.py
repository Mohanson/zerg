# -*- coding: utf-8 -*-
import sys

from zerg.settings import MODULE_DIR
from zerg import DocumentFpath, Handler

sys.path.append(MODULE_DIR.parent.parent.joinpath('eggs'))

if __name__ == '__main__':
    document = DocumentFpath(r'C:\Users\Mohanson\PycharmProjects\forward_manage\resources\documents\开发后台启动.md')
    document.execute(Handler.SetAuthor('Mohanson'))
    document.execute(Handler.SetTitle())
    document.execute(Handler.SetDirectory())
    document.execute(Handler.DrawCode())
    document.generate_fpath(r'C:\Users\Mohanson\PycharmProjects\forward_manage\resources\documents\开发后台启动.html')