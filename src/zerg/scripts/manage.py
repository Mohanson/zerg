# -*- coding: utf-8 -*-
import argparse
import importlib
import os

import saika.path


def list_sub_commands():
    return_list = []
    subdir = saika.path.abspath('./subs', os.path.dirname(__file__))
    subfolder = saika.path.Folder(subdir)
    for i in subfolder.files('*.py'):
        return_list.append(i.basename[0: -(len(i.ext) + 1)])
    return_list.remove('__init__')
    return return_list


def main():
    parser = argparse.ArgumentParser(prog='zerg')
    parser.add_argument('--version', action='version', version='%(prog)s')
    parser.add_argument('sub', help='sub command', choices=list_sub_commands())
    parser.add_argument('remaining', nargs=argparse.REMAINDER, help='all arguments to sub command')
    args = parser.parse_args()

    sub_module = importlib.import_module('zerg.scripts.subs.' + args.sub)
    sub_module.run(args.remaining)