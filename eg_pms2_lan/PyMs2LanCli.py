#!/usr/bin/env python3
import argparse
import json
import logging
import sys

from eg_ms2_lan.PyMs2LanLib import PyMs2Lan


def add_plug_arg(parser_obj):
    parser_obj.add_argument('plug', type=int, metavar='plug', choices=range(0, 4))


def parse_args():
    config_set = '--config' in sys.argv
    parser = argparse.ArgumentParser(description='Control a EG-PMS2-LAN plug board')

    parser.add_argument('--config', type=str, metavar='config', required=config_set,
                        help='json config file containing keys:'
                             '\nhost, port and password')

    parser.add_argument('-H', '--host', type=str, metavar='host', required=not config_set)
    parser.add_argument('-p', '--port', type=int, metavar='port', required=not config_set)
    parser.add_argument('-P', '--password', type=str, metavar='password', required=not config_set)

    subparsers = parser.add_subparsers(dest='cmd')

    subparsers.add_parser('status')
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

    logging.basicConfig(format='%(levelname)s:%(message)s')

    try:
        arguments = parse_args()

        host = None
        port = None
        password = None

        if arguments.config:
            conf = None
            with open(arguments.config, 'r') as conf_file:
                conf = json.load(conf_file)
            host = conf['host']
            port = conf['port']
            password = conf['password']
        elif arguments.config == '':
            raise FileNotFoundError
        else:
            host = arguments.host
            port = arguments.port
            password = arguments.password

        pmslan = PyMs2Lan(host, port, password)

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
    except FileNotFoundError:
        logging.error(f'config file not found')
    except KeyError:
        logging.error(f'wrong config file format')
