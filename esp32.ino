// ESP32 code to read EMG sensor and send data via Serial

const int emgPin = 34;  // Analog input pin for EMG sensor (GPIO34 is input-only)
const int baudRate = 9600;

void setup() {
  Serial.begin(baudRate);
  delay(2000);  // Wait for serial connection to stabilize
}

void loop() {
  int emgValue = analogRead(emgPin);  // Read analog EMG value (0-4095)
  
  Serial.println(emgValue);  // Send value as a line over serial
  
  delay(10);  // Sampling rate ~100 Hz (adjust as needed)
}
