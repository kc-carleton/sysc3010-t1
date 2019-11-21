 /*
  Door Controller
*/

#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

byte macAddress[] = {0x90, 0xA2, 0xDA, 0x0F, 0x3B, 0x9D};
IPAddress local_ip(192, 168, 123, 200);
IPAddress AS_ip(192, 168, 123, 202);
unsigned int local_port = 161;
unsigned int AS_port = 161;
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

  // initalize Udp communication
  if (Ethernet.begin(macAddress) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    for (;;);
  } else {
    Serial.println("Ethernet configuration successful.");
  }
  
  Ethernet.begin(macAddress, local_ip);
  Udp.begin(local_port);
  
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
    sendUDPPacket("ack", AS_ip, AS_port);
    delay(5000);
    while (readDoorSensor()) {
      delay(10);
    }
    lockDoor();
    sendUDPPacket("closed", AS_ip, AS_port);
  } else if (action == -1) {
    Serial.println("ERROR: Unknown action");
  }
  delay(100);
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
  char inBuffer[1];
  
  Serial.println("Listening for UDP Message");
  
  // receive packet but return if empty (no packet)
  int packetSize = Udp.parsePacket();
  if (!packetSize) {
    return 0;
  } else {
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
    Udp.read(inBuffer, 1);
    Serial.print("Contents: ");
    Serial.println(inBuffer);
    
    if (inBuffer[0] == '1') {
      return 1;
    } else {
      return-1;
    }
  }
}

/**
 * Send a udp message with the given string at the specified ip and port
 */
void sendUDPPacket(String message, IPAddress ip, unsigned int port) {
  Serial.print("Sending message to ");
  for (int i = 0; i < 4; i++) {
      Serial.print(ip[i], DEC);
      if (i < 3) {
      Serial.print(".");
    }
  }
  Serial.print(" on port ");
  Serial.println(port);
  Udp.beginPacket(ip, port);
  Udp.println(message);
  Udp.endPacket();
}

//////////////////////////////////////////////////////////////////////////////////////////
// Test functions
/////////////////////////////////////////////////////////////////////////////////////////

/**
 * Run all hardware tests
 */
void run_all_tests() {
  Serial.println("Testing deadbolt unlock...");
  test_deadbolt_unlock();
  delay(1000);
  Serial.println("Testing magnetic sensor...");
  test_magnetic_sensor();
  delay(1000);
  Serial.println("Testing deadbolt lock...");
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
