from hashlib import sha256
from matrixKeypad_RPi_GPIO import keypad
from time import sleep


kp = keypad()


def read_keypad():
    '''Will read user inputs from the keypad and save them in a Python tuple. 
    The tuple format is (user_code, hashed_passcode, safe number)'''
    
    keys = []
    
    # Get 9 key presses: 4 digit user code, 4 digit passcode, 1 digit safe number.
    count = 0
    while count != 3:
        keypress = get_digit()
        if keypress == '#':
            count += 1
        keys.append(keypress)
        sleep(0.5)
    
    print(verify_user_credentials(keys))
    #user_code = str(keys[0]) + str(keys[1]) + str(keys[2]) + str(keys[3])
    #passcode = str(keys[4]) + str(keys[5]) + str(keys[6]) + str(keys[7])
    #safe_number = str(keys[8])

    #return (user_code, passcode, safe_number)


def get_digit():
    # poll for key press
    key = None
    while key == None:
        key = kp.getKey()
    return key


def hash_passcode(passcode):
    '''Will hash the user entered passcode using SHA256 hashing algorithm.'''
    hash_object = sha256(passcode.encode())
    hash_digest = hash_object.hexdigest()
    return hash_digest


def set_LED(success):
    '''Set the LED to a colour based on the success parameter. If the success 
    is True, set the LED to green, otherwise set it to red.'''


def send_user_data_udp(user_code, hashed_passcode, safe_number):
    '''Will send a DATA packet to the Access System over UDP with the user credentials.'''


def receive_udp_ack():
    '''Wait for an acknowledgment packet from the Access System.'''
    return False


def verify_user_credentials(user_credentials):
    '''Verify user credentials match with expected format for credentials.'''
    if len(user_credentials) >= 12:
        if user_credentials[4] == '#' and user_credentials[9] == '#' and user_credentials[-1] == '#':
            user_code = user_credentials[0:4]
            passcode = user_credentials[5:9]
            safe_number = user_credentials[10:-1]
            if (all(isinstance(item, int) for item in user_code) and 
                    all(isinstance(item, int) for item in passcode) and 
                    all(isinstance(item, int) for item in safe_number)):
                return True
    return False


read_keypad()
