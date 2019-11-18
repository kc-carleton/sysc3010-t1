 /*
  Door Controller
*/

#include <Ethernet.h>
#include <EthernetUdp.h>

byte macAddress[] = {0xDE, 0xAD, 0xEF, 0xED};
IPAddress ip(192, 168, 123, 177);
int localPort = 8888;
EthernetUDP Udp;

int sensorPin = 2;
int deadboltPin = 9;
bool doorLocked = true;

/*
 * Setup UDP communication and peripheral pins
 */
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  // initalized Udp communication
  Ethernet.begin(macAddress, ip);
  Udp.begin(localPort);
  
  // set the sensor pin to be a pullup input
  pinMode(sensorPin, INPUT_PULLUP);
  // set the deadbolt pin to be an output
  pinMode(deadboltPin, OUTPUT);

//  Serial.println("Running hardware tests...");
//  run_all_tests();
}

//////////////////////////////////////////////////////////////////////////////////////////
// Main program loop
/////////////////////////////////////////////////////////////////////////////////////////

/**
 * Main DoorController program loop. This loop is repeated indefinitely.
 */
void loop() {
  // wait and receive UDP messages from AccessSystem
  int action = getUDPPacket();  
  
  // message to unlock door
  if (action == 1) {
    unlockDoor();
    // sendUDPPacket();
    delay(5000);
    while (readDoorSensor()) {
      delay(10);
    }
    lockDoor();
    // sendUDPPacket();
  } else {
    Serial.println("ERROR: Unknown action");
  }
  delay(10000);
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
 * Wait for and receive a UDP message
 */
int getUDPPacket() {
  char inBuffer[UDP_TX_PACKET_MAX_SIZE];
  char outBuffer[] = "acknowledged";

  // receive packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i = 0; i < 4; i++) {
      Serial.print(remote[i], DEC);
      if (i < 3) {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read packet contents into buffer
    Udp.read(inBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.print("Contents: ");
    Serial.println(inBuffer);

    // send a reply to acknowledge the message was received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(outBuffer);
    Udp.endPacket();
    
    
//    return inBuffer; 
    return 1;
  }
  delay(10);
}

void sendUDPPacket() {
  
}

//////////////////////////////////////////////////////////////////////////////////////////
// Test functions
/////////////////////////////////////////////////////////////////////////////////////////

/**
 * Run all hardware tests
 */
void run_all_tests() {
  test_deadbolt_unlock();
  test_magnetic_sensor();
  test_deadbolt_lock();
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
    delay(1000);
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
