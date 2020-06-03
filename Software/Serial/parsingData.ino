/*
Parsing Data

The purpose of this program is to parse data that is sent to the Arduino from the Jetson. This is an important part of the serial communication process between
the Jetson and Arduino because the Jetson sends the four motor PWM signals together as an array of characters in the form "<pwm1|pwm2|pwm3|pwm4>". For the
Arduino to use this data to set motor speeds, it needs to parse the data into the four PWM signals and convert them to integers. This code covers specifically
how the Arduino indentifies the four PWM signals and how they are converted to integers.

For simplicity purposes, the data is just declared in this program rather than having it being sent from a different program. Because of this, the start and
end markers (< and >) are not included in the data character array. If you are interested in how data is actually recieved by the Arduino, please refer to the
serialRead.ino program.

last modified 06/03/2020
by Anirudh Bali
*/

int numData; //stores integer form of parsed sent data

void setup() {
  Serial.begin(115200); //Starting serial for testing purposes
  while(!Serial) {
    ; //waiting for serial port to connect
  }
}

void loop() {
  char data[] = "1234|1567|1789|2000"; //data from jetson, representative of the four motor values being sent to arduino "pwm1|pwm2|pwm3|pwm4"
  char * pch; //pointer to parse the sent data

  pch = strtok (data, "|"); //get first token, function works by reading each char and storing in pch until it reads "|"
  while(pch != NULL) {
    numData = atoi(pch); //converts pch to an integer
    Serial.print(pch); //prints pch
    Serial.print("     ");
    Serial.println(numData); //prints integer form of pch
    pch = strtok (NULL, "|"); //get next token
  }
  delay(5000);
}
