#!/usr/bin/env python
import socket


class ProtocolError(Exception):
    pass


class PyMs2Lan:
    HANDSHAKE = b'\x11'
    PLUG_COUNT = 4

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = self.__encode_password(password)
        self.challenge = None
        self.upnp_socket = None
        self.__plug_changes = {}

    def __connect(self):
        self.upnp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.upnp_socket.connect((self.host, self.port))

    def __disconnect(self):
        self.upnp_socket.close()

    def __read(self):
        return self.upnp_socket.recv(4)

    def __send_array(self, array):
        self.upnp_socket.send(bytearray(array))

    def __handshake(self):
        self.upnp_socket.send(self.HANDSHAKE)
        self.challenge = self.__read()
        self.__send_array(self.__handle_challenge_request())

    def __handle_challenge_request(self):
        """
        calc response from password and challenge
        :return: list
        List of 4 bytes with calcuated values
        """
        part1 = (self.password[2] ^ self.challenge[0]) * self.password[0] ^ \
                (self.password[4] << 8 | self.password[6]) ^ self.challenge[2]
        part2 = (self.password[3] ^ self.challenge[1]) * self.password[1] ^ \
                (self.password[5] << 8 | self.password[7]) ^ self.challenge[3]

        return [
            part1 & 0xFF,
            part1 >> 8 & 0xFF,
            part2 & 0xFF,
            part2 >> 8 & 0xFF
        ]

    def __encode_password(self, password):
        """
        password will be filled with spaces
        to a fixed size of 8
        map of coresponding ascii number of char
        :param password: str
        :return: list<int>
        """
        return bytes(map(ord, password.ljust(8)[:8]))

    def __encode_plug_states(self, decoded_states):
        state_list = []
        for k, v in decoded_states.items():
            if v:
                state_list.append(1)  # state on
            else:
                state_list.append(2)  # state off
        # this is pretty ugly too
        encoded = []
        for t in range(0, 4):
            encoded.append(
                (
                        (
                                self.password[0] ^ (self.challenge[3] + (self.challenge[2] ^ state_list[3 - t]))
                        ) + self.password[1]) & 0xFF
            )
        return encoded

    def __decode_plug_states(self, encoded_states):
        """
        decode received bytes
        :param encoded_states:
        :return:
        """
        decoded_bytes = []
        for t in range(0, 4):
            decoded_bytes.append(
                (self.challenge[2] ^
                 (
                         (self.password[0] ^
                          (encoded_states[t] - self.password[1])
                          ) - self.challenge[3]
                 )
                 ) & 0xFF
            )

        decoded_states = {}
        # a b 0 0 0 0 a b
        # a:1 b:0 when socket is off 0x82
        # a:0 b:1 when socket is on 0x41
        # sockets in reverse row
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

    def __read_plug_states(self):
        return self.__decode_plug_states(self.__read())

    def __write_plug_states(self, plug_states):
        self.__send_array(self.__encode_plug_states(plug_states))

    def set_plug_state(self, plug, enabled=True):
        try:
            assert isinstance(plug, int)
            if plug < self.PLUG_COUNT:
                self.__plug_changes[plug] = enabled
            else:
                raise ProtocolError('')
        except AssertionError:
            raise ProtocolError('Wrong plug index type. Must be int! 0 <= plug < PLUG_COUNT')

    def communicate(self):
        self.__connect()
        self.__handshake()
        plug_states = self.__read_plug_states()
        for plug, change in self.__plug_changes.items():
            plug_states[plug] = change
        self.__write_plug_states(plug_states)
        self.__disconnect()
        return plug_states
