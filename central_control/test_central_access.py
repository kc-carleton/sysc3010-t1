from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import create_autospec

def normal_operation_1():
    test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
    mock_d = create_autospec(check_database_authentication, return_value=True)

    success = mock_d(test_data)
    send_ack_kc(success)

    return True

def normal_operation_2():
    test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
    mock_d = create_autospec(check_database_authentication, return_value=False)

    success = mock_d(test_data)
    send_ack_kc(success)

    return True


def normal_operation_3():
    test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
    mock_d = create_autospec(check_database_authentication, return_value=True)

    success = mock_d(test_data)
    command = create_command(success)
    send_pkt(command, dc_address, dc_port)

    return True

def normal_operarion_4():
    wait_dc_ack()

    return True

def incorrect_data_to_AS_1():

