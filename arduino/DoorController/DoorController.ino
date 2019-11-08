 /*
  Door Controller
*/

#include <Ethernet.h>
#include <EthernetUdp.h>

byte macAddress[] = {0xDE, 0xAD, 0xEF, 0xED};
IPAddress ip(192, 168, 1, 177);
int localPort = 8888;
EthernetUDP Udp;

int sensorPin = 2;
int deadboltPin = 9;

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
}

void loop() {
  retractDeadbolt();
  delay(5000);
  while (readSensor()) {}
  Serial.println("Door closed");
  lockDeadbolt();
  
  delay(1000);
}


/*
 * Read the state of the magnetic sensor.
 * Return true if the sensor is closed.
 */
bool readSensor() {
  // read the input pin:
  int sensorState = digitalRead(sensorPin);
  return sensorState ? true : false;
}

void retractDeadbolt() {
  digitalWrite(deadboltPin, HIGH);
}

void lockDeadbolt() {
  digitalWrite(deadboltPin, LOW);
}


void getUDPPacket() {
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
  }
  delay(10);
}

void sendUDPPacket() {
  
}
