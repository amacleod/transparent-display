void setup() {
    Serial.begin(9600);
    Serial.println("Arduino is ready");
}

void loop() {
  while (!Serial.available()) {
    delay(100);
  }
  read_and_echo();
}

void read_and_echo() {
  String s = Serial.readStringUntil("\n");
  String response = s.substring(0, s.length() - 1);
  Serial.println(response);
}
