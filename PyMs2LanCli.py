#!/usr/bin/env python3
from sys import argv

from PyMs2LanLib import PyMs2Lan


def print_usage():
    programm = argv[0].split('/')[-1:][0]
    print(f'Usage: {programm} command <plug>')
    print('Commands:')
    print('enable - enable a plug')
    print('disable - disable a plug')
    print('status - disable a plug')
    print()
    print('<plug>:')
    print(f'number between 0 and {PyMs2Lan.PLUG_COUNT - 1}')
    exit(1)


def index_error():
    print('invalid plug index!')
    print()
    print_usage()
    exit(1)


def set_state(enabled, p):
    print('{0} plug no. {1}'.format('Enabling' if enabled else 'Disabling', p))
    pmslan = PyMs2Lan('192.168.1.10', 5000, '1234')
    pmslan.set_plug_state(p, enabled)
    pmslan.communicate()


def get_states():
    pmslan = PyMs2Lan('192.168.1.10', 5000, '1')
    pmslan.communicate()


if __name__ == '__main__':
    argv = [argv[0], 'disable', 3]
    cmd = None
    plug = None

    if len(argv) > 1:
        cmd = argv[1]
    if len(argv) == 3:
        try:
            if 0 <= int(argv[2]) < PyMs2Lan.PLUG_COUNT:
                plug = argv[2]
            else:
                raise ValueError
        except ValueError:
            index_error()

    if cmd == 'status':
        get_states()
    elif cmd == 'enable' and plug is not None:
        set_state(True, plug)
    elif cmd == 'disable' and plug is not None:
        set_state(False, plug)
    else:
        print_usage()
