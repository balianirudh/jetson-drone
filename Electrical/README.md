# Electrical System

## Flight Controller

The drone carries an NVIDIA Jetson TX2 onboard. This is used as the main flight controller of the drone. The Jetson is capable of doing the necessary computation for video processing and the control system of the drone. Its high computing power made it perfect for the task of creating an autonomous drone and implementing an LQR controller.

Alongside the Jetson, an Arduino Uno is responsible for communicating the motor PWM signals to each ESC. After going through several calculations, the Jetson sends the respective PWM signal of each motor to the Arduino to set the speed of each motor.

"add picture of full electronics system here"

## Sensors

There are 3 main sensors on the drone that give it the ability to do what it can do. A BNO055 IMU is connected to the Jeston's GPIO pins. This is necessary to read the current pitch, roll, and yaw angles to make adjustments to maintain a specific orientation. Along with this, 2 cameras are onboard. The main camera is a downward facing USB camera. This camera is meant to identify the path of the desired trajectory for the drone. Using the identified path and the current trajectory of the drone, I am able to calculate the error angle. This angle is used by the LQR controller to calculate the new angular velocities of each motor. 

"add pictures of cameras onboard"

