import mock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import create_autospec
import unittest
from udp_utils import *
from central_access import *

class TestAccessSystem(unittest.TestCase):
    @mock.patch('udp_utils.send_pkt', return_value=True)
    def test_normal_operation_1(self, n_send_pkt):
        test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
        mock_d = create_autospec(check_database_authentication, return_value=True)

        success = mock_d(test_data)
        send_ack_kc(str(success))

        return True

    @mock.patch('udp_utils.send_pkt', return_value=True)
    def test_normal_operation_2(self, n_send_pkt):
        test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
        mock_d = create_autospec(check_database_authentication, return_value=False)

        success = mock_d(test_data)
        send_ack_kc(str(success))

        return True

    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    def test_normal_operation_3(self, n_send_pkt, n_receive_pkt):
        test_data = {'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}
        mock_d = create_autospec(check_database_authentication, return_value=True)

        success = mock_d(test_data)
        ack = create_ack(success)
        n_receive_pkt.return_value = ack, ''
        
        unlock_safe(1, 1)

        return True

    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.decode_ack', return_value=1)
    def test_normal_operarion_4(self, n_send_pkt, n_receive_pkt, n_decode_ack):
        #wait_dc_ack(1, 555)
        return True

    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_1(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_data("")
        dec, err = decode_data(data)
        self.assertEqual(err, 'no_json_data')

        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)


    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_2(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_ack(True)
        dec, err = decode_data(data)
        self.assertEqual(err, 'incorrect_data_opcode')
        
        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)

    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_3(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_data({"h": 1})
        data = data.decode('utf-8')[0:-1].encode('utf-8')
        dec, err = decode_data(data)
        self.assertEqual(err, 'no_null_termination')
        
        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)

    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_3(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_data({"h": 1})
        data = data.decode('utf-8')[0:-1].encode('utf-8')
        dec, err = decode_data(data)
        self.assertEqual(err, 'no_null_termination')
        
        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_4(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_data({"h": 1})
        dec, err = decode_data(None)
        self.assertEqual(err, 'empty_packet')
        
        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_data_to_AS_5(self, n_send_pkt, n_receive_pkt, n_create_error):
        data = create_data({"h": 1})
        dec, err = decode_data(data)
        self.assertEqual(err, 'incorrect_json')
        
        n_receive_pkt.return_value = data, ''
        p = PortListener()
        p.get_json_data()

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_ack_to_AS_1(self, n_send_pkt, n_receive_pkt, n_create_error):
        ack = create_data({"h": 1})
        dec, err = decode_ack(ack)
        self.assertEqual(err, 'incorrect_ack_opcode')

        n_receive_pkt.return_value = ack, ''
        wait_dc_ack(1, 1)

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_ack_to_AS_2(self, n_send_pkt, n_receive_pkt, n_create_error):
        ack = create_ack(True)
        ack = ack.decode('utf-8')[0:-1].encode('utf-8')
        dec, err = decode_ack(ack)
        self.assertEqual(err, 'no_null_termination')

        n_receive_pkt.return_value = ack, ''
        wait_dc_ack(1, 1)

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_ack_to_AS_3(self, n_send_pkt, n_receive_pkt, n_create_error):
        ack = '{}\0\0'.format(PacketType.ACK.value).encode()
        dec, err = decode_ack(ack)
        self.assertEqual(err, 'no_command')

        n_receive_pkt.return_value = ack, ''
        wait_dc_ack(1, 1)

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_ack_to_AS_4(self, n_send_pkt, n_receive_pkt, n_create_error):
        ack = None
        dec, err = decode_ack(ack)
        self.assertEqual(err, 'empty_packet')

        n_receive_pkt.return_value = ack, ''
        wait_dc_ack(1, 1)

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)
    
    @mock.patch('udp_utils.send_pkt', return_value=True)
    @mock.patch('udp_utils.receive_pkt')
    @mock.patch('udp_utils.create_error', return_value='x')
    def test_incorrect_ack_to_AS_5(self, n_send_pkt, n_receive_pkt, n_create_error):
        ack = create_ack('Boo')
        dec, err = decode_ack(ack)
        self.assertEqual(err, 'inavlid_command')

        n_receive_pkt.return_value = ack, ''
        wait_dc_ack(1, 1)

        self.assertEqual(n_send_pkt.call_count, 1)
        self.assertEqual(n_create_error.call_count, 1)

    def test_unreciprocated_command(self):
        pass

if __name__ == '__main__':
    unittest.main()
