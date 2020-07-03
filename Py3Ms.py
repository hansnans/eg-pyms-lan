#!/usr/bin/env python
import socket


def calcuate_challenge_response(password, challenge):
    """
    calc response from password and challenge
    :param password: bytes
    password of switch
    :param challenge: bytes
    challenge received from switch after sending handshake
    :return: list
    List of 4 bytes with calcuated values
    """
    part1 = (password[2] ^ challenge[0]) * password[0] ^ \
            (password[4] << 8 | password[6]) ^ challenge[2]
    part2 = (password[3] ^ challenge[1]) * password[1] ^ \
            (password[5] << 8 | password[7]) ^ challenge[3]

    return [
        part1 & 0xFF,
        part1 >> 8 & 0xFF,
        part2 & 0xFF,
        part2 >> 8 & 0xFF
    ]


def read_4_bytes(sock):
    return sock.recv(4)


def decode_states(challenge, password):
    # old statement
    # st = [(challenge[2] ^ ((password[0] ^ (socket_states[t] - password[1])) - challenge[3])) & 0xFF for t in range(0, 4)]
    decoded_states = []
    for t in range(0, 4):
        decoded_states.append(
            (challenge[2] ^ ((password[0] ^ (socket_states[t] - password[1])) - challenge[3])) & 0xFF
        )

    return decoded_states


states = {1: True}
host = ('192.168.1.10', 5000)
handshake = bytes('\x11', encoding='utf-8')

# password will be filled with spaces
# to a fixed size of 8
# map of coresponding ascii number of char
passwd = bytes(map(ord, '1'.ljust(8)[:8]))

upnp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with upnp_sock:
    upnp_sock.connect(host)
    upnp_sock.send(handshake)
    #  receive 4 bytes and save them in a list as ascii numbers
    chg = read_4_bytes(upnp_sock)
    response = calcuate_challenge_response(passwd, chg)

    upnp_sock.send(bytearray(response))
    socket_states = read_4_bytes(upnp_sock)
    new_states = decode_states(chg, passwd)
    print(new_states)
    # a b 0 0 0 0 1 0
    # a:1 b:0 when socket is off
    # a:0 b:1 when socket is on
    # sockets in reverse row
