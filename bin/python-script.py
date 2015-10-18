#!"C:\Users\Mohanson\AppData\Local\Programs\Python\Python35-32\python.exe"

import sys

sys.path[0:0] = [
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\src',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\saika-0.3.8-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\jinja2-2.8-py3.5.egg',
  'c:\\users\\mohanson\\pycharmprojects\\zerg\\eggs\\markupsafe-0.23-py3.5.egg',
  ]


_interactive = True
if len(sys.argv) > 1:
    _options, _args = __import__("getopt").getopt(sys.argv[1:], 'ic:m:')
    _interactive = False
    for (_opt, _val) in _options:
        if _opt == '-i':
            _interactive = True
        elif _opt == '-c':
            exec(_val)
        elif _opt == '-m':
            sys.argv[1:] = _args
            _args = []
            __import__("runpy").run_module(
                 _val, {}, "__main__", alter_sys=True)

    if _args:
        sys.argv[:] = _args
        __file__ = _args[0]
        del _options, _args
        with open(__file__, 'U') as __file__f:
            exec(compile(__file__f.read(), __file__, "exec"))

if _interactive:
    del _interactive
    __import__("code").interact(banner="", local=globals())
