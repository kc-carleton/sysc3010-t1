import threading
from firebase import firebase
import json
import random
import udp_utils 
import datetime
import socket

# Hardcoded values for system
firebase = firebase.FirebaseApplication('https://sysc3010-t1.firebaseio.com/', None)
kc_port = 10001
dc_port = 161
kc_address = ''
safes_map = {"2": '10.1.1.2'}

def check_database_authentication(user_cred):
   """
   Checks user credentials with database.

   Parameters
   ---------
   user_cred: dict
       User credentials dictionary that includes user code, user passcode, and safe number

   Returns
   ------
   bool
       True or False on database validation.
   """
   result = firebase.get('/users', None) 
   if result is None:
       return False, ''
   for key in result:
       user = result[key]
       if user is None:
           return False, ''
       if str(user_cred.get('user_code')) != str(user.get('user_code')):
           continue
       credentials = user.get('credentials')
       if credentials is None:
           return False, user_cred.get('user_name')
       for i in range(len(credentials)):
           credential = credentials[i]
           # Check if credentials match database
           if str(credential.get('hashed_passcode')) == str(user_cred.get('hashed_passcode')) and str(credential.get('safe')) == str(user_cred.get('safe')):
               failed_login_count = 0
               out = {'failed_login_count': failed_login_count, 'hashed_passcode': credential.get('hashed_passcode'), 'safe': credential.get('safe')}
               firebase.patch('/users/{}/credentials/{}'.format(key, i), out)
               return True, user_cred.get('user_name')
           else:
               # If don't match, make sure user tried to access safe with incorrect passcode
               if(str(credential.get('safe')) == str(user_cred.get('safe'))):
                   failed_login_count = int(credential.get('failed_login_count')) + 1
                   out = {'failed_login_count': failed_login_count, 'hashed_passcode': credential.get('hashed_passcode'), 'safe': credential.get('safe')}
                   firebase.patch('/users/{}/credentials/{}'.format(key, i), out)
                   return False, user_cred.get('user_name')
   return False, ''

def update_database_logs(user, safe, success):
    """
    Update logs of user access to safes on database.

    Parameters
    ---------
    user: Str
        User code
    safe: int
        safe number
    success: bool
        Whether the credentials were successfully verified.

    Returns
    ------
    void
    """
    if user is None:
        return 
    update = {'user': user, 'access_time': datetime.datetime.now(), 'success': success}

    print("Updating database logs with entry: {}".format(update))

    result = firebase.get('/safes', None)
    if result is None:
        result = {}

    error = firebase.post('/safes/{}'.format(safe), update)

def unlock_safe(socket, safe, thread_port, dc_address):
    """
    Unlocks safe by sending request to unlock safe to Door Controller

    Parameters
    ---------
    socket: Socket
        socket to send request
    safe: int
        safe number
    thread_port: int
        Port of current thread
    dc_address: Str
        IP address of Door Controller

    Returns
    ------
    Str
        Ack from Door Controller
    """
    command, _ = udp_utils.create_command(True)
    udp_utils.send_pkt(socket, command, dc_address, dc_port)
    ack = wait_dc_ack(socket, safe, thread_port)
    return ack

def send_ack_kc(success):
    """
    Unlocks safe by sending request to unlock safe to Door Controller

    Parameters
    ---------
    socket: Socket
        socket to send request
    safe: int
        safe number
    thread_port: int
        Port of current thread
    dc_address: Str
        IP address of Door Controller

    Returns
    ------
    Str
        Ack from Door Controller
    """
    ack = udp_utils.create_ack(success)
    udp_utils.send_pkt(ack, kc_address, kc_port)

def wait_dc_ack(socket, safe, thread_port):
    """
    Wait Ack from Door Controller

    Parameters
    ---------
    socket: Socket
        socket to send possible error
    safe: int
        safe number
    thread_port: int
        Port of current thread

    Returns
    ------
    Str
        Ack from Door Controller
    """
    ack = None
    # Wait for ack from dc. Error occurs if timeout happens 3 times.
    for i in range(3):
        buf, address = udp_utils.receive_pkt(socket, thread_port)
        if buf != None:
            break
    if address is None:
        print("Timeout occured when waiting for DC")
    elif buf is None: # Error
        error_mes = udp_utils.create_error(address)
        udp_utils.send_pkt(socket, error_mes, address, dc_port)
    else:
        ack, error = udp_utils.decode_ack(buf)
        if ack is None: # Error
            error_mes = udp_utils.create_error(error)
            udp_utils.send_pkt(socket, error_mes, address, dc_port)
    return ack

def action_thread(safe, hashed_passcode, user_code, sender_port, sender_ip):
    """
    Action thread main logic. Verify credentials in database, update database, unlock
    safe.

    Parameters
    ---------
    safe: int
        safe number
    hashed_passcode: Str
        User hashed passcodes
    user_code: Str
        User code
    sender_port: Str
        Port of Keypad Controller
    sender_ip: Str
        IP address of Keypad Controller

    Returns
    ------
    void
    """

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    thread_port = random.randint(1000,50000)
    server_address = ('', thread_port)
    s.bind(server_address)

    # Verify credentials in database and update database logs
    success, user_name  = check_database_authentication({'user_code': user_code, 'hashed_passcode': hashed_passcode, 'safe': safe})
    update_database_logs(user_code, safe, success)

    # Unlock safe upon successfull credentials
    if(success and safes_map.get(safe) != None):
        ack = unlock_safe(s, safe, thread_port, safes_map.get(safe))
        print("Ack got back is: {}".format(ack))
        if not ack:
            success = False
    
    # Create and send ack to Keypad Controller
    ack_kc = udp_utils.create_ack(success)

    print("Sending to: address: {} port: {}".format(sender_ip, kc_port))

    udp_utils.send_pkt(s, ack_kc, sender_ip[0], kc_port)
    
    if(success and safes_map.get(safe) is not None):
        wait_dc_ack(s, safe, thread_port)
    print("Closed connection")
    s.close()

class ActionThread(threading.Thread):
    """
    Action thread to start logic for unlocking safe.
    """
    def __init__(self, safe, hashed_passcode, user_code, sender_port, sender_ip):
        """
        Init constructor for the class

        Parameters
        ---------
        safe: int
            safe number
        hashed_passcode: Str
            User hashed passcodes
        user_code: Str
            User code
        sender_port: Str
            Port of Keypad Controller
        sender_ip: Str
            IP address of Keypad Controller

        Returns
        ------
        void
        """
        super(ActionThread, self).__init__()
        self.safe = safe
        self.hashed_passcode = hashed_passcode
        self.user_code = user_code
        self.sender_port = sender_port
        self.sender_ip = sender_ip

    def run(self):
        """
        Run function for thread creation.
        """
        action_thread(self.safe, self.hashed_passcode, self.user_code, self.sender_port, self.sender_ip)


class PortListener:
    """
    Port listener for requests from Keypad Controller
    """

    def __init__(self):
        """
        Init constructor for the class
        """
        open_port = 10010
        self.open_port = open_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_json_data(self):
        """
        Get user credentials json data from Keypad Controller
        
        Returns
        ------
        ret: bool
            Success if json data was extracted
        data: Dict
            User credentials dict from Keypad Controller
        address: tuple
            IP address and port of Keypad Controller 
        """
        ret = True
        print("Waiting for packet")
        buf, address = udp_utils.receive_pkt(self.socket, self.open_port)
        print("Got packet")
        data, err = udp_utils.decode_data(buf)
        print("{} {}".format(data, err))
        if(address is None or address[0] is None):
            ret = False
        elif(data is None): # An error occurred
            error_mes = udp_utils.create_error(err)
            try:
                udp_utils.send_pkt(self.socket, error_mes, address[0], kc_port)
            except:
                print("Failed to send error packet, recovered")
                pass
            ret = False
        return ret, data, address

    def listen_port(self):
        """
        Main loop to listen for requests from Keypad Controller.
        """
        # Listen to port using UDP
        server_address = ('', self.open_port)
        self.socket.bind(server_address)
        while True:
            ret, data, address = self.get_json_data()
            if ret:
                json_data = json.loads(data)
                self.spawn_action_thread(kc_port, address, json_data)
    
    def spawn_action_thread(self, sender_port, sender_ip, received_message):
        """
        Spawn action thread to handel Keypad Controller request

        Parameters
        ---------
        sender_port: Str
            Port of Keypad Controller
        sender_ip: Str
            IP address of Keypad Controller
        received_message: Dict
            Json dict of user credentials

        Returns
        ------
        void
        """
        # Listen port will call this to spawn a thread using multiprocessing
        thread = ActionThread(received_message['safe_number'], received_message['hashed_passcode'], received_message['user_code'], sender_port, sender_ip)
        thread.start()


def main():
    p = PortListener()
    p.listen_port()

if __name__ == '__main__':
    main()

