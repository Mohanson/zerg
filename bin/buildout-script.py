#!"C:\Users\Mohanson\AppData\Local\Programs\Python\Python35-32\python.exe"

import sys
sys.path[0:0] = [
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\setuptools-18.4-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\zc.buildout-2.4.5-py3.5.egg',
  ]

import zc.buildout.buildout

if __name__ == '__main__':
    sys.exit(zc.buildout.buildout.main())
