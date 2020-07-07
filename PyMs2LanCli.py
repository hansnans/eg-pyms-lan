#!/usr/bin/env python3
from sys import argv


def print_usage():
    print(f'Usage: {argv[0]} command <plug>')
    print('Commands:')
    print('enable - enable a plug')
    print('disable - disable a plug')


if __name__ == '__main__':
    argv = [argv[0], 'disables', '1']
    if len(argv) < 3:
        print('Not enough arguments')
        exit(1)

    cmd = argv[1]
    plug = argv[2]

    if cmd == 'enable':
        print(cmd)
    elif cmd == 'disable':
        print(cmd)
    elif cmd == 'status':
        print(cmd)
    else:
        print_usage()
