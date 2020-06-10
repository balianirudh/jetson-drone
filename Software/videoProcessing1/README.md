# Path Detection (Version 1)

The purpose of this program was to identify a marked path as the desired path of the drone. After the video is taken by a downward facing USB camera, the video is processed by this program using OpenCV in python. The program not only identifies the desired path but it also calculates the angle error between the desired and current path of the drone. This angle is used in the controller of the drone to keep it moving along the desired path. However, when using this program in practice, there was too much lag in the video processing for the drone to accurately know its orientation at any given time. This called for a change in the path detection software that is covered in videoProcessing2. 

## Acknowledgements

Credit for the path detection development goes to kemfic on GitHub. His post about "Simple Lane Detection" on hackster.io inspired the path detection aspect of this project. I have used his path detection software as the foundation of my path detection program in this project. If you are interested in an indepth article on how kemfic developed his simple lane detection software please refer to his article on hackster.io (https://www.hackster.io/kemfic/simple-lane-detection-c3db2f).

"add picture of cv pipeline here"
