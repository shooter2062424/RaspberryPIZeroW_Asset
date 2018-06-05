void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}
String s = "";
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    char c = Serial.read();
    if(c == '\n'){
      Serial.println(s);
      s = "";
    } else{
      s += c;
    }
  }
}
