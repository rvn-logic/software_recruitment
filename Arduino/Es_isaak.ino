#include <Arduino.h>

const int JOYSTICK_PIN = A2;
const byte INSTRUCTION_GOAL_POS = 0x1E;

unsigned long lastSampleTime = 0;
const unsigned long SAMPLE_INTERVAL = 100;

void setup() {
  Serial.begin(19200);
  pinMode(JOYSTICK_PIN, INPUT);
}

void loop() {
  unsigned long CurrentTime = millis();

  if (CurrentTime - lastSampleTime >= SAMPLE_INTERVAL) {
    lastSampleTime = CurrentTime;
    
    int joystickVal = analogRead(JOYSTICK_PIN);
    int targetPos = map(joystickVal, 0, 1023, 818, 511);

    uint16_t pos16 = (uint16_t)targetPos;
    Serial.write(INSTRUCTION_GOAL_POS);
    Serial.write((uint8_t)(pos16 & 0xFF));
    Serial.write((uint8_t)((pos16 >> 8) & 0xFF));
  }
}
