#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

#define DIR_PIN 11
#define PUL_PIN 10
#define STEP_DELAY 1000  // Adjust this value for speed (lower value = faster speed)
#define RUN_TIME 1000  // 2 seconds

// Create a SoftwareSerial object
// SoftwareSerial mySerial(8, 9); // RX, TX pins


// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

void setup() {
  pinMode(DIR_PIN, OUTPUT);
  pinMode(PUL_PIN, OUTPUT);
  // Set up the LCD's number of columns and rows:
  lcd.begin(16, 2); // Assuming a 16x2 LCD

  // Start serial communication at 9600 baud (using the hardware serial)
  Serial.begin(9600);
  //  mySerial.begin(9600);

  // Print an initial message
  lcd.print("Waiting for data...");
}

void loop() {
  // Check if there is any data available to read from the hardware serial (pin 0)
  if (Serial.available() > 0) {
    String inputData = Serial.readString();  // Read the incoming data as a sj,bnm,  ,
      runMotor(LOW);
    }
    else{
      runMotor(HIGH);
    }
    lcd.clear();
    lcd.print(inputData);  // Print the received serial data on the LCD
    delay(1000);  // Adjust delay as neededhello
    
  }
  else{
    delay(1000);  // Adjust delay as needed
    Serial.println("No data...");
  }
}


void runMotor(int direction) {
  // Set the direction of the motor (LOW = one direction, HIGH = opposite direction)
  digitalWrite(DIR_PIN, direction);  // Change to HIGH for reverse direction

  Serial.println("RUUNNING MOTOR");

  unsigned long startTime = millis();  // Record the start time

  // Run the motor for 2 seconds (2000 ms)
  while (millis() - startTime < RUN_TIME) {
    // Create a pulse signal for the stepper motor
    digitalWrite(PUL_PIN, HIGH);
    delayMicroseconds(STEP_DELAY);  // Adjust for speed of motor
    digitalWrite(PUL_PIN, LOW);
    delayMicroseconds(STEP_DELAY);  // Adjust for speed of motor
  }
}
