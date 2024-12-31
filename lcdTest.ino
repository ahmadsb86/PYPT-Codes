#include <LiquidCrystal.h>
#include <Keypad.h>

// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(1, 2, 3, 4, 5, 6);

// Define the number of rows and columns for the keypad
const byte ROWS = 4; // Four rows
const byte COLS = 3; // Three columns

// Define the keymap
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

// Connect keypad ROW0, ROW1, ROW2, ROW3 to these Arduino pins.
byte rowPins[ROWS] = {13, 12, 11, 10};

// Connect keypad COL0, COL1, COL2 to these Arduino pins.
byte colPins[COLS] = {9, 8, 7};




void setup() {
  // Set up the LCD's number of columns and rows:
  lcd.begin(16, 2); // Assuming a 16x2 LCD
  // Print "Hello, World!" to the LCD.
  lcd.print("Hello, Worldly m!");
}

void loop() {
  // Nothing to do here; the message stays on the screen.
}
