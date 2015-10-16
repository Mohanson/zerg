# -*- coding: utf-8 -*-
import argparse

import zerg.win32env


help = """
Sample:
    saika env -u/-s: show all environment variables
    saika env author: show the value of variable author
    saika env -(f)d author: (forece)delete variable author
    saika env author Mohanson: set variable author = Mohanson
"""


def run(args):
    parser = argparse.ArgumentParser(description='handle environment variable', prog='saika.env',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, epilog=help)
    parser.set_defaults(user=True, truth=False)
    parser.add_argument('-u', '--user', dest='user', action='store_true', help='choose user scope(default)')
    parser.add_argument('-s', '--system', dest='user', action='store_false', help='choose system scope')
    parser.add_argument('-d', '--delete', dest='delete', action='store_true', help='delete')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='execute command without ask')

    parser.add_argument('key', nargs='?')
    parser.add_argument('value', nargs='?')
    args = parser.parse_args(args)

    if args.user:
        env = zerg.win32env.Environment.from_user()
    else:
        env = zerg.win32env.Environment.from_system()

    if not args.key:
        for i in env.enums(args.truth):
            values = zerg.win32env.trans_string_to_list(i[1])
            if len(values) == 1:
                info = values[0]
            else:
                info = ('\n' + ' ' * 12).join(values)
            blocks = ' ' * (12 - len(i[0])) if (12 - len(i[0])) > 0 else 2
            print('%s%s%s' % (i[0], blocks, info))
    elif args.key and not args.value:
        if args.delete:
            # delete key
            if args.force:
                env.delete(args.key)
            else:
                choose = input('you want to delete %s, y/n? ' % args.key)
                if choose == 'y':
                    env.delete(args.key)
        else:
            # show key value
            try:
                print(env.get(args.key, args.truth))
            except FileNotFoundError:
                print('None')
    elif args.key and args.value:
        env.set(args.key, args.value)
