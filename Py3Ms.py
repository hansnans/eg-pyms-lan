#!/usr/bin/env python
import socket


class ProtocolError(Exception):
    pass


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


def decode_states(encoded_states, challenge, password):
    # old statement
    # st = [(challenge[2] ^ ((password[0] ^ (socket_states[t] - password[1])) - challenge[3])) & 0xFF for t in range(0, 4)]
    decoded_bytes = []
    for t in range(0, 4):
        temp = encoded_states[t]
        decoded_bytes.append(
            (challenge[2] ^
             (
                     (password[0] ^
                      (encoded_states[t] - password[1])
                      ) - challenge[3]
             )
             ) & 0xFF
        )

    decoded_states = {}
    for b in reversed(range(len(decoded_bytes))):
        if decoded_bytes[b] == 0x41:  # state on
            state = True
        elif decoded_bytes[b] == 0x82:  # state off
            state = False
        else:
            raise ProtocolError()

        # bytes are in reverse row. Has to be reverted
        # byte 1 -> socket 4
        # byte 2 -> socket 3
        # byte 3 -> socket 2
        # byte 4 -> socket 1
        decoded_states[3 - b] = state

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
    new_states = decode_states(socket_states, chg, passwd)
    print(new_states)
    # a b 0 0 0 0 1 0
    # a:1 b:0 when socket is off
    # a:0 b:1 when socket is on
    # sockets in reverse row
