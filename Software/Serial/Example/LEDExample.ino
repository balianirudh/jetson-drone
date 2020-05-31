/*
LED Example

This LED Example code is meant to demonstrate the serial communication between the Jetson and Arduino. With this program, there is no need to calculate
different motor values, instead, a C++ file sends data that tells the Arduino how long to turn off its onboard LED. This code is responsible for reading the
data sent to the Arduino and then turning off the LED based on the data sent. What you should see is that the onboard LED should turn on for 2 seconds and 
turn off for 3 seconds in a loop.

This code is an adaptation of Robin2's Serial Input Basics Arduino Forum post in 2015 in which he outlines how to read several characters from Arduino's
serial channel. Credit goes to him for developing the recvData() function that I have used in this program. If you are interested in learning different serial
communication techniques in Arduino I would refer you to Robin2's forum post: https://forum.arduino.cc/index.php?topic=288234.0

If you are interested learning how to write data from a C++ file to an Arduino, refer to my GitHub repository for the Jetson drone project in the software
folder: https://github.com/balianirudh/jetson-drone

last modified 5/30/2018
by Anirudh Bali
*/

const byte numChars = 6; //number of bytes being sent to Arduino. For LED example data sent in the form "<led delay in milliseconds>"
char receivedChars[numChars]; //received data

char * pch; //pointer token used to convert chars to int
int receivedInts; //integer form of data received

boolean newData = false;

void setup() {
  Serial.begin(115200); //can increase baud rate if there is too much of a delay between sending and receiving
  while(!Serial) {
    ; //waiting for serial port to connect
  }
  pinMode(LED_BUILTIN, OUTPUT); //initializing build in LED on Arduino
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); //turning LED on for 2 seconds
  delay(2000);
  recvData(); //reading and storing incoming data
  ledOff(receivedChars); //turning LED off based on data received
  setNewData(); //resetting so new incoming data can be read
}

//the recvData() function is called when data sent to the Arduino needs to be read and stored
void recvData() {
  static boolean recvInProgress = false;
  static byte ndx = 0; //index for received bytes
  char startMarker = '<'; //sent data starts with this marking
  char endMarker = '>'; //sent data ends with this marking
  char rc; //the current byte being read and then added to receivedChars

  //only want to read data when serial port is available and when there is new data to read
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read(); //reads a byte of sent data
    
    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc; //adds the new byte of data to the receivedChars
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1; 
        }
      } else {
        receivedChars[ndx] = '\0'; //end the string once all data has been added
        recvInProgress = false;
        ndx = 0;
        newData = true; //needed for setNewData()
      }
    }
    else if (rc == startMarker) {
      recvInProgress = true; //once the start marker is read we start storing the data
    }
  }
}

//setNewData() is to set newData to false after data is read so new incoming data can be read usig recvData()
void setNewData() {
  if (newData == true) {
    newData = false;
  }
}

//function for converting receivedChars into integers and then turning off LED with data (input of function is receivedChars)
void ledOff(char inputChars[]) {
  pch = inputChars; //setting pointer token as the received data
  receivedInts = atoi(pch); //converts pch to integer so it can be used as a delay
  digitalWrite(LED_BUILTIN, LOW); //turns off LED for whatever time is sent to Arduino 
  delay(receivedInts);
}
