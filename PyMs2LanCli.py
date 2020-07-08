#!/usr/bin/env python3
import argparse

from PyMs2LanLib import PyMs2Lan


def add_plug_arg(parser_obj):
    parser_obj.add_argument('plug', type=int, metavar='plug', choices=range(0, 4))


def parse_args():
    parser = argparse.ArgumentParser(description='Control a EG-PMS2-LAN plug board')

    parser.add_argument('-H', '--host', type=str, metavar='host', required=True)
    parser.add_argument('-p', '--port', type=int, metavar='port', required=True)
    parser.add_argument('-P', '--password', type=str, metavar='password', required=True)

    subparsers = parser.add_subparsers(dest='cmd')

    sub_status = subparsers.add_parser('status')
    sub_enable = subparsers.add_parser('enable')
    sub_disable = subparsers.add_parser('disable')

    add_plug_arg(sub_enable)
    add_plug_arg(sub_disable)

    return parser.parse_args()


def format_states(states_obj):
    assert isinstance(states_obj, dict)
    width = 6
    print('| '.join(['Plug'.center(width), 'State'.center(width)]))
    print('-' * (width * 2))

    for k, v in states_obj.items():
        status = 'ON' if v else 'OFF'
        print('| '.join([str(k).center(width), status.ljust(width)]))


if __name__ == '__main__':
    try:
        arguments = parse_args()

        pmslan = PyMs2Lan(
            arguments.host,
            arguments.port,
            arguments.password)

        if arguments.cmd == 'enable':
            print(f'Enabling plug no. {arguments.plug}')
            pmslan.set_plug_state(arguments.plug, True)
        elif arguments.cmd == 'disable':
            print(f'Disabling plug no. {arguments.plug}')
            pmslan.set_plug_state(arguments.plug, False)

        states = pmslan.communicate()
        if arguments.cmd == 'status':
            format_states(states)
    except KeyboardInterrupt:
        pass
