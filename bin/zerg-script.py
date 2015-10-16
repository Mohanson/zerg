#!"C:\Users\Mohanson\AppData\Local\Programs\Python\Python35\python.exe"

import sys
sys.path[0:0] = [
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\src',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\saika-0.3.6-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\pygments-2.0.2-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\beautifulsoup4-4.4.0-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\jinja2-2.8-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\markdown-2.6.2-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\markupsafe-0.23-py3.5.egg',
  ]

import zerg.scripts.manage

if __name__ == '__main__':
    sys.exit(zerg.scripts.manage.main())
