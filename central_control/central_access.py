from multiprocessing import Process
from firebase import firebase

firebase = firebase.FirebaseApplication('https://sysc3010-t1.firebaseio.com/', None)

def start_open_door_action():
    pass

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
    print(result)
    #safe_data = result.get(safe)

    #if safe_data is None:
    #    safe_data = {}

    error = firebase.post('/safes/{}'.format(safe), update)

def unlock_safe(safe):
    pass

def send_ack_kc(success):
    pass

def send_error_kc(error_message):
    pass

def wait_dc_ack(safe):
    pass

def notify_admin(number_of_tries, user_code, safe):
    pass

def action_thread(safe, hashed_passcode, user_code, sender_port, sender_ip):
    pass





class PortListener:

    def __init__(self):
        open_port = 30

    def listen_port(self):
        # Listen to port using UDP
        pass
    def spawn_action_thread(self, sender_port, sender_ip, received_message):
        # Listen port will call this to spawn a thread using multiprocessing
        pass


print(check_database_authentication({'user_name':'michael', 'hashed_passcode': '3973', 'safe': 1}))
#update_database_logs('michael', 627262, 1, True)
