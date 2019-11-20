from enum import Enum
import socket
import json


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
    data = '{}\0{}\0'.format(PacketType.DATA.value, str(json_data))
    return data.encode()


def decode_data(encoded):
    '''Returns the data stored inside the provided data packet byte array.
    PARAM encoded: a byte array representing the data in the DATA packet.
    RETURN a string representing the data which was sent in the DATA packet.'''
    if encoded is None:
        return None, 'empty_packet'
    if encoded.decode('utf-8')[-1] != '\0':
        return None, 'no_null_termination'
    data = encoded.decode('utf-8').split('\0')
    if data[0] != PacketType.DATA.value:
        return None, 'incorrect_data_opcode'
    if data[1] == '':
        return None, 'no_json_data'
    try:
        json_data = json.loads(data[1])
        keys = json_data.keys()
        if len(keys) != 3:
            raise Exception("err")
        if 'user_name' not in keys or 'hashed_passcode' not in keys or 'safe' not in keys:
            raise Exception("err")
    except:
        return None, 'incorrect_json'
    return data[1], ''


def create_ack(ack_type):
    data = '{}\0{}\0'.format(PacketType.ACK.value, str(ack_type))
    return data.encode()


def decode_ack(encoded):
    if encoded is None or len(encoded) < 6:
        return None, 'empty_packet'
    if encoded.decode('utf-8')[-1] != '\0':
        return None, 'no_null_termination'
    data = encoded.decode('utf-8').split('\0')
    if data[0] != PacketType.ACK.value:
        return None, 'incorrect_ack_opcode'
    if len(data) == 0:
        return None, 'no_command'
    if len(data) != 3:
        return None, 'inavlid_command'
    return data[1]


def create_command(cmd):
    if cmd is None:
        return None
    elif len(cmd) == 0:
        return None
    data = '{}\0{}\0'.format(PacketType.COMMAND.value, str(cmd))
    return data.encode()


def decode_command(encoded):
    if encoded is None:
        return None, 'empty_packet'
    data = encoded.decode('utf-8').split('\0')
    if data[0] != PacketType.COMMAND.value:
        return None, 'Not a COMMAND packet'
    if len(data) != 3:
        return None, 'byte array format is incorrect'
    if len(data[1]) == 0:
        return None, 'Command field is empty'
    return data[1], ''


def create_error(error_message):
    if error_message is None:
        return None
    elif len(error_message) == 0:
        return None
    data = '{}\0{}\0'.format(PacketType.ERROR.value, str(error_message))
    return data.encode()


def decode_error(encoded):
    if encoded is None:
        return None, 'empty_packet'
    data = encoded.decode('utf-8').split('\0')
    if data[0] != PacketType.ERROR.value:
        return None, 'Not an ERROR packet'
    if len(data) != 3:
        return None, 'byte array format is incorrect'
    return data[1], ''


class PacketType(Enum):
    DATA = '0x01'
    ACK = '0x02'
    COMMAND = '0x03'
    ERROR = '0x04'


