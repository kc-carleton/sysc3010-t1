from enum import Enum
import socket


def send_pkt(data, ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip_address, port)
    s.sendto(data, server_address)


def receive_pkt(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', port)
    s.bind(server_address)
    buf, address = s.recvfrom(port)
    return (buf, address)


def create_data(json_data):
    '''Returns a byte array for a data packet containing the json string provided.
    PARAM json_data: A json string representing the data to be sent.
    RETURN a byte array representing the data in the DATA packet to be sent.'''
    if json_data is None:
        return None
    data = 'DATA\0{}\0'.format(str(json_data))
    return data.encode()


def decode_data(encoded):
    '''Returns the data stored inside the provided data packet byte array.
    PARAM encoded: a byte array representing the data in the DATA packet.
    RETURN a string representing the data which was sent in the DATA packet.'''
    if encoded is None:
        return None
    data = encoded.decode('utf-8').split('\0')
    if data[0] != 'DATA':
        print('Not a data packet')
        return None
    return data[1]


def create_ack(ack_type):
    data = 'ACK\0{}\0'.format(str(ack_type.value))
    return data.encode()


def decode_ack(encoded):
    if encoded is None or len(encoded) < 6:
        return None
    data = encoded.decode('utf-8').split('\0')
    if data[0] != 'ACK':
        print('Not an ACK packet')
        return None
    if len(data) != 3:
        print('byte array format is incorrect')
        return None
    return data[1]


def create_command(cmd):
    if cmd is None:
        return None
    elif len(cmd) == 0:
        return None
    data = 'COMMAND\0{}\0'.format(str(cmd))
    return data.encode()


def decode_command(encoded):
    if encoded is None:
        return None
    data = encoded.decode('utf-8').split('\0')
    if data[0] != 'COMMAND':
        print('Not a COMMAND packet')
        return None
    if len(data) != 3:
        print('byte array format is incorrect')
        return None
    if len(data[1]) == 0:
        return None
    return data[1]


def create_error(error_message):
    if error_message is None:
        return None
    elif len(error_message) == 0:
        return None
    data = 'ERROR\0{}\0'.format(str(error_message))
    return data.encode()


def decode_error(encoded):
    if encoded is None:
        return None
    data = encoded.decode('utf-8').split('\0')
    if data[0] != 'ERROR':
        print('Not an ERROR packet')
        return None
    if len(data) != 3:
        print('byte array format is incorrect')
        return None
    return data[1]


class PacketType(Enum):
    DATA = 'DATA'
    ACK = 'ACK'
    COMMAND = 'COMMAND'
    ERROR = 'ERROR'


