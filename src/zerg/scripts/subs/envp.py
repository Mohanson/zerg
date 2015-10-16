# -*- coding: utf-8 -*-
import argparse
import zerg.win32env

help = """
Sample:
    saika envp -u/-s: show all paths in scope user or system
    saika envp c:/: add c:/ to environment path
    saika envp -(f)d index: (forece)delete the path by given index
    saika envp -c: clean paths
"""


def run(args):
    parser = argparse.ArgumentParser(description='handle environment path', prog='saika.envp',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, epilog=help)

    parser.set_defaults(user=True, truth=False)
    parser.add_argument('-u', '--user', dest='user', action='store_true', help='choose user scope(default)')
    parser.add_argument('-s', '--system', dest='user', action='store_false', help='choose system scope')
    parser.add_argument('-t', '--truth', dest='truth', action='store_true', help='replace constant in value')
    parser.add_argument('-d', '--delete', dest='delete', action='store_true', help='delete')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='execute command without ask')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true', help='cleanup envp')

    parser.add_argument('args', nargs='*')
    args = parser.parse_args(args)

    if args.user:
        envp = zerg.win32env.EnvironmentPath.from_user()
    else:
        envp = zerg.win32env.EnvironmentPath.from_system()

    if not args.args and not args.clean:
        for index, i in enumerate(envp.enums(args.truth)):
            print('%s   %s' % (index, i))
    else:
        for arg in args.args:
            if args.delete:
                if args.force:
                    envp.delete(int(arg))
                else:
                    choose = input('you want to delete %s, y/n? ' % envp.enums()[int(arg)])
                    if choose == 'y':
                        envp.delete(int(arg))
            else:
                envp.add(arg)
    if args.clean:
        envp.cleanup()
        for index, i in enumerate(envp.enums(args.truth)):
            print('%s   %s' % (index, i))
