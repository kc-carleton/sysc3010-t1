from multiprocessing import Process


def start_open_door_action():
    pass

def check_database_authentication():
    pass

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






class PortListener:

    def __init__(self):
        open_port = 30

    def listen_port(self):
        # Listen to port using UDP
        pass
    def spawn_action_thread(self, sender_port, sender_ip, received_message):
        # Listen port will call this to spawn a thread using multiprocessing




