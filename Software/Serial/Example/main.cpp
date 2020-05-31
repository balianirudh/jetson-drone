/*
LED Example

This LED Example code is meant to demonstrate the serial communication between the Jetson and Arduino. With this program, there is no need to calculate
different motor values, instead, a C++ file sends data that tells the Arduino how long to turn off its onboard LED. This code is responsible for sending the
data to the Arduino from a C++ program that is used to turn off an LED. What you should see is that the Arduino's onboard LED should turn on for 2 seconds and 
turn off for 3 seconds in a loop.

last modified 5/31/2018
by Anirudh Bali
*/

#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;

char serialPortFilename[] = "COM3"; //file path of Arduino, in Windows this is a COM port, in Linux it follows the
                                    // form /dev/ttyACM0 or /dev/ttyUSB0 depending on the distribution

int main()
{
    FILE * serPort = fopen(serialPortFilename, "w"); //defining and opening Arduino COM port, "w" indicates writing to this file

    if(serPort == NULL)
    {
        printf("ERROR"); //check if Arduino file path exists, if it doesn't send ERROR message
        return 0;
    }

    char writeBuffer[] = {"<3000>"}; //data that is being sent to Arduino, need start and end markers (<, >)
                                     //this data is used as a delay for how long the Arduino onboard LED stays off
                                     //delay is in milliseconds
    fwrite(writeBuffer, sizeof(char), sizeof(writeBuffer), serPort); //sending data to Arduino
    //first parameter is array of elements, second is size of each element, third is number of elements,
    //fourth is Arduino file path

    fclose(serPort); //close Arduino file path once data is sent
    return 0;
}
