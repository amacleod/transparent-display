


byte byteRead;

void setup() {
  // set up once
Serial.begin(9600);
delay(500);

}

void loop() {
  // run main code repeatedly


  if(Serial.available( )){
  byteRead = Serial.read();
  Serial.write(byteRead);
  
  }
  delay(1000);
  Serial.write("end");
}


//================================================================================
