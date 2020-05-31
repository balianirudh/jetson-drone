# Serial Communication with Arduino LED

Serial communication is vital to the function of the drone because without it the drone would not receive motor commands. I am sure there is a way to use the GPIO pins of the Jetson to send PWM signals to the motor controllers, however, the Arduino platform makes this task straightforward. 

The purpose of this example to is demonstrate how the serial communication between the Jetson TX2 and Arduino Uno work on the drone. With this example, there is no need to calculate specific motor values or have the full ROS package of this project set up. Instead it uses the Arduino's onboard LED to demonstrate how data is being sent from a C++ program to the Arduino.

Note that even though the C++ program only sends data to the Arduino once, the Arduino's onboard LED continously blinks using data that was only sent once. This is because the variable receivedInts (in Arduino program) is never written over with new data and the function that blinks the LED is in a loop.
