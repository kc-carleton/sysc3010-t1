from enum import Enum
import socket
import json
import select

def send_pkt(s, data, ip_address, port):
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip_address, port)
    s.sendto(data, server_address)


def receive_pkt(s, port):
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #server_address = ('', port)
    #s.bind(server_address)

    s.setblocking(0)
    timeout_length = 60
    ready = select.select([s], [], [], timeout_length)
    if ready[0]:
        data, address = s.recvfrom(port)
        return data, address
    return None, 'socket timed out'


def create_data(json_data):
    '''Returns a byte array for a data packet containing the json string provided.
    PARAM json_data: A json string representing the data to be sent.
    RETURN a byte array representing the data in the DATA packet to be sent.'''
    if json_data is None:
        return None
    data = '{}{}\0'.format(PacketType.DATA.value, json.dumps(json_data))
    return data.encode()


def decode_data(encoded):
    '''Returns the data stored inside the provided data packet byte array.
    PARAM encoded: a byte array representing the data in the DATA packet.
    RETURN a string representing the data which was sent in the DATA packet.'''
    if encoded is None:
        return None, 'empty_packet'
    if len(encoded) == 0:
        return None, 'empty_byte_array'
    if encoded.decode('utf-8')[-1] != '\0':
        return None, 'no_null_termination'
   
    data_string = encoded.decode('utf-8')
    opcode = data_string[:4]
    data = data_string[4:].split('\0')[0]

    if opcode != PacketType.DATA.value:
        return None, 'incorrect_data_opcode'
    if data == '""':
        return None, 'no_json_data'
    try:
        json_data = json.loads(data)
        keys = json_data.keys()
        if len(keys) != 3:
            raise Exception("err")
        if 'user_code' not in keys or 'hashed_passcode' not in keys or 'safe_number' not in keys:
            raise Exception("err")
    except:
        return None, 'incorrect_json'
    return data, ''


def create_ack(success):
    data = '{}{}\0'.format(PacketType.ACK.value, str(success))
    return data.encode()


def decode_ack(encoded):
    if encoded is None or len(encoded) < 6:
        return None, 'empty_packet'
    if not (encoded.decode('utf-8')[-1] == '\0' or encoded.decode('utf-8')[-1] == '0'):
        return None, 'no_null_termination'
   
    data_string = encoded.decode('utf-8')
    opcode = data_string[:4]
    data = data_string[4:].split('\0')[0]
    print("Data: {}".format(data))

    if opcode != PacketType.ACK.value:
        return None, 'incorrect_ack_opcode'
    if len(data) == 0:
        return None, 'no_command'
    if 'True' not in data and 'False' not in data:
        return None, 'inavlid_command'
    if 'True' in data:
        return True ,''
    else:
        return False, ''


def create_command(cmd):
    if cmd is None:
        return None, 'empty_command'
    if cmd is '':
        return None, 'empty_command'
    data = '{}{}\0'.format(PacketType.COMMAND.value, str(cmd))
    return data.encode(), ''


def decode_command(encoded):
    if encoded is None:
        return None, 'empty_packet'
    if len(encoded) == 0:
        return None, 'empty_packet'
    if encoded.decode('utf-8')[-1] != '\0':
        return None, 'no_null_termination'

    data_string = encoded.decode('utf-8')
    opcode = data_string[:4]
    data = data_string[4:].split('\0')[0]
    print("Command packet, data is {} opcode is {}".format(data,opcode))
    if opcode != PacketType.COMMAND.value:
        return None, 'Not a COMMAND packet'
    if len(data) == 0:
        return None, 'Command field is empty'
    return data, ''


def create_error(error_message):
    if error_message is None:
        return None
    elif len(error_message) == 0:
        return None
    data = '{}{}\0'.format(PacketType.ERROR.value, str(error_message))
    return data.encode()


def decode_error(encoded):
    if encoded is None:
        return None, 'empty_packet'
    if len(encoded) is 0:
        return None, 'empty_packet'
    if encoded.decode('utf-8')[-1] != '\0':
        return None, 'no_null_termination'

    data_string = encoded.decode('utf-8')
    opcode = data_string[:4]
    data = data_string[4:].split('\0')[0]
    
    if opcode != PacketType.ERROR.value:
        return None, 'Not an ERROR packet'
    if len(data) == 0:
        return None, 'Empty error message'
    return data, ''


class PacketType(Enum):
    DATA = '0x01'
    ACK = '0x02'
    COMMAND = '0x03'
    ERROR = '0x04'


