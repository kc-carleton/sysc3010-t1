from hashlib import sha256
from keypad_library import keypad
from time import sleep
import udp_utils as utils
import RPi.GPIO as GPIO

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
    
    # Verify the users credentials before continuing.
    if verify_user_credentials(keys) is False:
        print('Invalid user credential format')
        return

    user_code = keys[0:4]
    passcode = keys[5:9]
    safe_number = keys[10:-1]

    return (user_code, passcode, safe_number)


def get_digit():
    '''poll for key press and return the key which was pressed'''
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
    
    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(5, GPIO.OUT) # green LED
    GPIO.setup(6, GPIO.OUT) # red LED

    #if success
    if success is True:
        GPIO.output(5, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(5, GPIO.LOW)
    else:
        GPIO.output(6, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(6, GPIO.LOW)


def send_user_data_udp(user_code, hashed_passcode, safe_number, ip_addr, port):
    '''Will send a DATA packet to the Access System over UDP with the user credentials.'''
    login_info = '{{user_code:{},hashed_passcode:{},safe_number:{}}}'.format(user_code, hashed_passcode, safe_number)
    data_pkt = utils.create_data(login_info)
    utils.send_pkt(data_pkt, ip_addr, port)


def receive_udp_ack():
    '''Wait for an acknowledgment packet from the Access System.'''
    port = 8080
    buf, address = utils.receive_pkt(port)
    ack_data = utils.decode_ack(buf)
    if ack_data is None:
        print('Error receiving ACK packet')
        return False
    return True


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
                set_LED(True)
                return True
    set_LED(False)
    return False


