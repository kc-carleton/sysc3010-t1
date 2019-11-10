

def read_keypad():
    '''Will read user inputs from the keypad and save them in a Python tuple. 
    The tuple format is (user_code, hashed_passcode, safe number)'''
    return ("", "", "")


def hash_passcode(passcode):
    '''Will hash the user entered passcode using SHA256 hashing algorithm.'''
    return ""


def set_LED(success):
    '''Set the LED to a colour based on the success parameter. If the success 
    is True, set the LED to green, otherwise set it to red.'''


def send_user_data_udp(user_code, hashed_passcode, safe_number):
    '''Will send a DATA packet to the Access System over UDP with the user credentials.'''


def receive_udp_ack():
    '''Wait for an acknowledgment packet from the Access System.'''
    return False


def verify_user_credentials():
    '''Verify user credentials match with expected format for credentials.'''
    return False



