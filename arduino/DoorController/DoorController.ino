 /*
  Door Controller
*/

#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

byte macAddress[] = {0x90, 0xA2, 0xDA, 0x0F, 0x3B, 0x9D};
IPAddress local_ip(10, 1, 1, 2);
IPAddress AS_ip(10, 1, 1, 1);
unsigned int local_port = 161;
unsigned int AS_port = 161;
EthernetUDP Udp;

int sensorPin = 2;
int deadboltPin = 9;
bool doorLocked = true;

int iter = 0;
char true_ack_msg[] = {'0', 'x', '0', '2', 'T', 'r', 'u', 'e', '\\', '0', '\0'};
char false_ack_msg[] = {'0', 'x', '0', '2', 'F', 'a', 'l', 's', 'e', '\\', '0', '\0'};

/*
 * Setup UDP communication and peripheral pins
 */
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  // set the sensor pin to be a pullup input
  pinMode(sensorPin, INPUT_PULLUP);
  // set the deadbolt pin to be an output
  pinMode(deadboltPin, OUTPUT);

  Serial.println("RUNNING HARDWARE TESTS...");
  run_all_tests();

  Serial.println("Configuring Ethernet...");
  // initalize Udp communication
  if (Ethernet.begin(macAddress) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    for (;;);
  } else {
    Serial.println("Ethernet configuration successful.");
  }
  
  Ethernet.begin(macAddress, local_ip);
  Udp.begin(local_port);
}

//////////////////////////////////////////////////////////////////////////////////////////
// Main program loop
/////////////////////////////////////////////////////////////////////////////////////////

/**
 * Main DoorController program loop. This loop is repeated indefinitely.
 */
void loop() {
  // wait and receive UDP messages from AccessSystem
  if (iter % 100 == 0) {
    Serial.println("Listening for UDP Message...");
  }
  int action = getUDPPacket();
  
  // if message to unlock door
  if (action == 1) {
    unlockDoor();
    sendUDPPacket(true_ack_msg, AS_ip, AS_port);
    delay(5000);
    int timer = 0;
    while (readDoorSensor()) {
      // if the DC gets a command to open the door while already open,
      // send a false ack msg to the AccessSystem
      int command = getUDPPacket();
      if (command == 1) {
        sendUDPPacket(false_ack_msg, AS_ip, AS_port);
      }
      delay(1000);
      // lock the safe after 60 seconds
      timer += 1;
      if (timer == 60) {
        break;
      }
    }
    lockDoor();
    // notify the AccessSystem that the safe is closed
    sendUDPPacket(true_ack_msg, AS_ip, AS_port);
  } else if (action == -1) {
    Serial.println("ERROR: Unknown action");
  }
  
  delay(100);
  iter += 1;
  if (iter == 100) {
    iter = 0;
  }
}


//////////////////////////////////////////////////////////////////////////////////////////
// DoorController functions
/////////////////////////////////////////////////////////////////////////////////////////

/*
 * Read the state of the magnetic sensor. Return true if the magnets are not connected.
 * Return false if connected.
 */
bool readDoorSensor() {
  int sensorState = digitalRead(sensorPin);
  return sensorState ? true : false;
}

/**
 * Place a HIGH voltage on the deadbolt pin to retract the deadbolt
 */
void unlockDoor() {
  digitalWrite(deadboltPin, HIGH);
  Serial.println("Unlocking Safe...");
}

/*
 * Place a LOW voltage on the deadbolt pin to lock the deadbolt
 */
void lockDoor() {
  digitalWrite(deadboltPin, LOW);
  Serial.println("Locking Safe...");
}

/**
 * Wait for and receive a UDP message. Returns 0 if no packet received,
 * 1 if unlock message received and -1 if unknown message
 */
int getUDPPacket() {
  char inBuffer[20];
  
  // receive packet but return if empty (no packet)
  int packetSize = Udp.parsePacket();
  if (!packetSize) {
    return 0;
  } else {
    Serial.print("Received packet of size ");
    Serial.print(packetSize);
    Serial.print(" From ");
    IPAddress remote = Udp.remoteIP();
    for (int i = 0; i < 4; i++) {
      Serial.print(remote[i], DEC);
      if (i < 3) {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    AS_port = Udp.remotePort();
    Serial.println(AS_port);
    

    // read packet contents into buffer
    Udp.read(inBuffer, 13);
    Serial.print("Contents: ");
    Serial.println(inBuffer);
    Serial.println();
    
    if (inBuffer[4] == 'T') {
      return 1;
    } else {
      return-1;
    }
  }
}

/**
 * Send a udp message with the given string at the specified ip and port
 */
void sendUDPPacket(char message[], IPAddress ip, unsigned int port) {
  Serial.print("Sending '");
  Serial.print(message);
  Serial.print("' to ");
  for (int i = 0; i < 4; i++) {
      Serial.print(ip[i], DEC);
      if (i < 3) {
      Serial.print(".");
    }
  }
  Serial.print(" on port ");
  Serial.println(port);
  Udp.beginPacket(ip, port);
  Udp.print(message);
  Udp.endPacket();
}

//////////////////////////////////////////////////////////////////////////////////////////
// Test functions
/////////////////////////////////////////////////////////////////////////////////////////

/**
 * Run all hardware tests
 */
void run_all_tests() {
  Serial.println();
  delay(1000);
  Serial.println("TESTING DEADBOLT UNLOCK...");
  test_deadbolt_unlock();
  
  Serial.println();
  delay(3000);
  Serial.println("TESTING MAGNETIC SENSOR...");
  test_magnetic_sensor();
 
  Serial.println();
  delay(3000);
  Serial.println("TESTING DEADBOLT LOCK...");
  test_deadbolt_lock();
  Serial.println();
  Serial.println("ALL TESTS COMPLETE... BOOTING SYSTEM...");
  Serial.println();
}


/**
 * Function to test unlocking the deadbolt.
 */
void test_deadbolt_unlock() {
  int action = mockGetUDPPacket();
  if (action == 1) {
    unlockDoor();
  }
}

/**
 * Function to test locking the deadbolt after it has been unlocked.
 */
void test_deadbolt_lock() {
  bool doorState = mockReadDoorSensor();
  if (!doorState) {
    lockDoor();
  }
}

/**
 * Function for testing magnetic sensor hardware. The monitor displays the state of the magnets.
 * This function runs for 10 seconds.
 */
void test_magnetic_sensor() {
  for (int i = 0; i < 10; i++) {
    int sensorState = digitalRead(sensorPin);
    if (sensorState) {
      Serial.println("Open");
    } else {
      Serial.println("Closed");
    }
    delay(500);
  }
}

/**
 * Mock function for receiving UDP Packet from AccessSystem.
 */
int mockGetUDPPacket() {
  return 1;
}

/**
 * Mock function to read doors as closed.
 */
bool mockReadDoorSensor() {
  return false;
}
