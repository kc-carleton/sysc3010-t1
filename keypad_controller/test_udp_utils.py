import pytest
import udp_utils as utils
import json


def test_create_data_1():
    json_string = None
    expected_result = None
    assert utils.create_data(json_string) == expected_result


def test_create_data_2():
    json_string = ''
    expected_result = b'0x01\0'
    assert utils.create_data(json_string) == expected_result


def test_create_data_3():
    json_string = 'testdata:test'
    expected_result = '0x01{}\0'.format(json_string).encode()
    assert utils.create_data(json_string) == expected_result


def test_decode_data_1():
    encoded = None
    expected_result = (None, 'empty_packet')
    assert utils.decode_data(encoded) == expected_result


def test_decode_data_2():
    encoded = 'incorrect\0format\0'.encode()
    expected_result = (None, 'incorrect_data_opcode')
    assert utils.decode_data(encoded) == expected_result


def test_decode_data_3():
    encoded = ''.encode()
    expected_result = None, 'empty_byte_array'
    assert utils.decode_data(encoded) == expected_result


def test_decode_data_4():
    data = '{"user_code":"1234","hashed_passcode":"placeholder_hash","safe_number":1}'
    encoded = '0x01{}\0'.format(data).encode()
    expected_result = data, ''
    assert utils.decode_data(encoded) == expected_result


def test_create_ack_1():
    expected_result = '0x02True\0'.encode()
    assert utils.create_ack(True) == expected_result


def test_create_ack_2():
    expected_result = '0x02False\0'.encode()
    assert utils.create_ack(False) == expected_result

# These tests are not needed anymore since create_ack takes a boolean now.
#def test_create_ack_3():
#    packetType = utils.PacketType.COMMAND
#    expected_result = 'ACK\0COMMAND\0'.encode()
#    assert utils.create_ack(packetType) == expected_result
#
#
#def test_create_ack_4():
#    packetType = utils.PacketType.ERROR
#    expected_result = 'ACK\0ERROR\0'.encode()
#    assert utils.create_ack(packetType) == expected_result


def test_decode_ack_1():
    encoded = '0x02True\0'.encode()
    expected_result = True, ''
    assert utils.decode_ack(encoded) == expected_result


def test_decode_ack_2():
    encoded = '0x02False\0'.encode()
    expected_result = True, ''
    assert utils.decode_ack(encoded) == expected_result


def test_decode_ack_3():
    encoded = None
    expected_result = None, 'empty_packet'
    assert utils.decode_ack(encoded) == expected_result


def test_decode_ack_4():
    encoded = b'ACK\0'
    expected_result = None, 'empty_packet'
    assert utils.decode_ack(encoded) == expected_result


def test_decode_ack_5():
    encoded = b'XYZ\0\0'
    expected_result = None, 'empty_packet'
    assert utils.decode_ack(encoded) == expected_result


def test_decode_ack_6():
    encoded = b'ACK\0\0'
    expected_result = None, 'empty_packet'
    assert utils.decode_ack(encoded) == expected_result


def test_create_command_1():
    test_command = 'opendoor=1'
    expected_result = b'0x03opendoor=1\0', ''
    assert utils.create_command(test_command) == expected_result


def test_create_command_2():
    test_command = ''
    expected_result = None, 'empty_command'
    assert utils.create_command(test_command) == expected_result


def test_create_command_3():
    test_command = None
    expected_result = None, 'empty_command'
    assert utils.create_command(test_command) == expected_result


def test_decode_command_1():
    encoded = None
    expected_result = None, 'empty_packet'
    assert utils.decode_command(encoded) == expected_result


def test_decode_command_2():
    encoded = b'ABCDE\0\0'
    expected_result = None, 'Not a COMMAND packet'
    assert utils.decode_command(encoded) == expected_result


def test_decode_command_3():
    encoded  = b''
    expected_result = None, 'empty_packet'
    assert utils.decode_command(encoded) == expected_result


def test_decode_command_4():
    encoded = b'0x03\0'
    expected_result = None, 'Command field is empty'
    assert utils.decode_command(encoded) == expected_result


def test_decode_command_5():
    test_cmd = 'testcmd=1'
    encoded = '0x03{}\0'.format(test_cmd).encode()
    expected_result = test_cmd, ''
    assert utils.decode_command(encoded) == expected_result


def test_create_error_1():
    error_msg = None
    expected_result = None
    assert utils.create_error(error_msg) == expected_result


def test_create_error_2():
    error_msg = ''
    expected_result = None
    assert utils.create_error(error_msg) == expected_result


def test_create_error_3():
    error_msg = 'test error message'
    expected_result = '0x04{}\0'.format(error_msg).encode()
    assert utils.create_error(error_msg) == expected_result


def test_decode_error_1():
    encoded = None
    expected_result = None, 'empty_packet'
    assert utils.decode_error(encoded) == expected_result


def test_decode_error_2():
    encoded = b''
    expected_result = None, 'empty_packet'
    assert utils.decode_error(encoded) == expected_result


def test_decode_error_3():
    encoded = b'invalid\0\0'
    expected_result = None, 'Not an ERROR packet'
    assert utils.decode_error(encoded) == expected_result


def test_decode_error_4():
    error_msg = 'test error'
    encoded = '0x04{}\0'.format(error_msg).encode()
    expected_result = error_msg, ''
    assert utils.decode_error(encoded) == expected_result


