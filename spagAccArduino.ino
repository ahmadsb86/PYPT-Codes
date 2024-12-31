// Define the pins for direction and pulse
#define DIR_PIN 11
#define PUL_PIN 10

// Define the speed (delay between pulses)
#define STEP_DELAY 1000  // Adjust this value for speed (lower value = faster speed)

// Time to run the motor in milliseconds
#define RUN_TIME 1000  // 2 seconds

void setup() {
  // Set the direction and pulse pins as output
  pinMode(DIR_PIN, OUTPUT);
  pinMode(PUL_PIN, OUTPUT);

  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available in the serial input buffer
  if (Serial.available() > 0) {

    char command = Serial.read();  // Read the incoming byte

    // Check if the character 'S' is typed
    if (command == 'B' || command == 'b') {
      // Run the motor for 2 seconds
      runMotor(LOW);
    }
    if (command == 'F' || command == 'f') {
      // Run the motor for 2 seconds
      runMotor(HIGH);
    }
  }
}

void runMotor(int direction) {
  // Set the direction of the motor (LOW = one direction, HIGH = opposite direction)
  digitalWrite(DIR_PIN, direction);  // Change to HIGH for reverse direction

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
