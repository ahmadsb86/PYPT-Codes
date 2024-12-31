#include <SoftwareSerial.h>

// Create a SoftwareSerial object
SoftwareSerial mySerial(0, 1); // RX, TX pins

void setup() {
  // Start serial communication with the laptop
  Serial.begin(9600);
  // Start software serial communication with Arduino 2
  mySerial.begin(9600);
}

void loop() {
  // Read the analog values from pins A0 and A1
  int valueA0 = analogRead(A0);
  int valueA1 = analogRead(A1);

  // Print the values to the serial monitor (laptop)
  Serial.print("A0: ");
  Serial.print(valueA0);
  Serial.print("\tA1: ");
  Serial.println(valueA1);

  // Send the values to Arduino 2 via SoftwareSerial
  mySerial.print("33A0: ");
  mySerial.print(valueA0);
  mySerial.print("\tA1: ");
  mySerial.println(valueA1);

  delay(500);  // Delay in milliseconds
}
