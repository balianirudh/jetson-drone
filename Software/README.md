# Software

The Jetson TX2 onboard the drone runs Ubuntu 16.04 LTS as the operating system. This gives a tremendous amount of flexibility in regard to how programs can be run on the machine. To fly, the drone is running several different programs that communicate with each other using a publisher-subscriber model. This is done through the robot operating system (ROS) framework to make it a seamless process.

"flowchart of publisher-subscriber model here. refer to portfolio"

## Mobility Control

There are two main controllers that have been implemented on the Jetson drone. The first is a nested PID controller for attitude control. Raw IMU data is processed through a Kalman filter to reduce noise from the IMU. This data is then used by the PID controller to stabilize the drone for any desired orientation.

Rather than using a PID controller for the line following aspect of the drone, I decided to implement an LQR controller. The LQR controller is responisble for calculating each motor's angular velocity to follow a given path. This controller was used because of how it is based on the state-space representation of the system. Unlike other controller, LQR taes into account the dynamics of the drone which is advantageous when trying to move in a specific way.

<p align="center"><img src=https://github.com/balianirudh/jetson-drone/blob/master/images/testingStand.png width=589 height=350></p>
<p align="center"> Drone on test stand for stability tuning </p>

## Vision System

There are two cameras onboard the Jetson drone; however, currently, only one is being used. The camera that is being used is the downward-facing USB camera. This camera is responsible for taking a live recording of what is below the drone. The video is then  analyzed using OpenCV to determine where the desired path is.

"add flowchart of lane detection"  "add picture of lane detection in action"
