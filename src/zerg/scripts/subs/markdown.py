# -*- coding: utf-8 -*-
import argparse
import os

import zerg.mkdown


def run(args):
    parser = argparse.ArgumentParser(prog='saika markdown')
    parser.set_defaults(list=True)
    parser.add_argument('-l', '--list', dest='list', action='store_true', help='set hinfos')
    parser.add_argument('-n', '--nolist', dest='list', action='store_false', help='don\'t set hinfos')
    parser.add_argument('dirs', nargs='+')
    args = parser.parse_args(args)

    for dir in args.dirs:
        m = zerg.mkdown.MarkDown.from_fpath(dir)
        if args.list:
            m.execute_analysis_hinfos()
        m.generate_fpath(os.path.join(os.path.dirname(dir), m.default_file_name))