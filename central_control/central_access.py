import threading
from firebase import firebase
import json
import random
import udp_utils 

firebase = firebase.FirebaseApplication('https://sysc3010-t1.firebaseio.com/', None)
kc_port = 5
dc_port = 5
kc_address = ''
dc_address = ''

def check_database_authentication(user_cred):
   result = firebase.get('/users', None) 
   if result is None:
       return False
   for key in result:
       user = result[key]
       if user is None:
           return False
       if str(user_cred.get('user_name')) != str(user.get('user_name')):
           return False
       credentials = user.get('credentials')
       if credentials is None:
           return False
       for credential in credentials:
           if str(credential.get('hashed_passcode')) == str(user_cred.get('hashed_passcode')) and str(credential.get('safe')) == str(user_cred.get('safe')):
               return True
   return False

def update_database_logs(user, access_time, safe, success):
    update = {'user': user, 'access_time': access_time, 'success': success}

    result = firebase.get('/safes', None)
    if result is None:
        result = {}

    error = firebase.post('/safes/{}'.format(safe), update)

def unlock_safe(safe, thread_port):
    command = udp_utils.create_command(True)
    udp_utils.send_pkt(command, dc_address, dc_port)
    ack = wait_dc_ack(safe, thread_port)

def send_ack_kc(success):
    ack = udp_utils.create_ack(success)
    udp_utils.send_pkt(ack, kc_address, kc_port)

def send_error_kc(error_message):
    error = udp_utils.create_error(error_message)
    udp_utils.send_pkt(error, kc_address, kc_port)

def start_open_door_action():
    command = udp_utils.create_command(True)

def wait_dc_ack(safe, thread_port):
    buf, address = udp_utils.receive_pkt(thread_port)
    ack, error = udp_utils.decode_ack(buf)
    if ack is None: # Error
        error_mes = udp_utils.create_error(error)
        udp_utils.send_pkt(error_mes, address, dc_port)
    return ack

def notify_admin(number_of_tries, user_code, safe):
    pass

def action_thread(safe, hashed_passcode, user_code, sender_port, sender_ip):
    thread_port = random.randint(1000,50000)

    success = check_database_authentication({'user_name': user_code, 'hashed_passcode': hashed_passcode, 'safe': safe})

    ack_kc = create_ack(success)

    if(success):
        unlock_safe(safe, thread_port)

    udp_utils.send_pkt(ack_kc, kc_address, kc_port)

class ActionThread(threading.Thread):
    def __init__(self, safe, hashed_passcode, user_name, sender_port, sender_ip):
        self.safe = safe
        self.hashed_passcode = hashed_passcode
        self.user_name = user_name
        self.sender_port = sender_port
        self.sender_ip = sender_ip

    def run(self):
        action_thread(self.safe, self.hashed_passcode, self.user_code, self.sender_port, self.sender_ip)


class PortListener:

    def __init__(self):
        self.open_port = 30

    def get_json_data(self):
        ret = True

        buf, address = udp_utils.receive_pkt(self.open_port)
        data, err = udp_utils.decode_data(buf)
        if(data is None): # An error occurred
            error_mes = udp_utils.create_error(err)
            udp_utils.send_pkt(error_mes, address, kc_port)
            ret = False
        return ret, data

    def listen_port(self):
        # Listen to port using UDP
        while True:
            ret, data = get_json_data()
            if ret:
                json_data = json.loads(data)
                self.spawn_action_thread(kc_port, address, json_data)
    
    def spawn_action_thread(self, sender_port, sender_ip, received_message):
        # Listen port will call this to spawn a thread using multiprocessing
        thread = ActionThread(received_message['safe'], received_message['hashed_passcode'], received_message['user_name'], sender_port, sender_ip)
        thread.start()


def main():
    p = PortListener()
    p.listen_port()

if __name__ == '__main__':
    main()

#print(check_database_authentication({'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}))
#update_database_logs('michael', 627262, 1, True)
