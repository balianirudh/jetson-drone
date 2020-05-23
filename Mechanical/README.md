# Mechancial System

## Frame

The first drone I designed featured laser cut acrylic arms and a top plate that were connected to the power distribtution board by 3D printed brackets. Although this was a sturdy frame and naturally stable due to its weight, it was too heavy for the motor and propeller system I was using. This gave the drone a very short flight time.

<p align="center"><img src="https://github.com/balianirudh/jetson-drone/blob/master/images/acrylicFrame.jpg" width="400" height="300"/></p>

For the Jetson Drone, I kept in mind speed, agility, and ease of use when designing the frame. Alogn with this, I designed the frame specifically to house the NVIDIA Jetson TX2 carrier board as it has a fairly large footprint compared to most flight controllers used in drones.

The keep the weight low, I decided to 3D print the entire frame. I initially planned to use thinner laser cut acrylic parts but after testing, the thin arcylic arms were too flexible. The frame is made out of two pieces that are held together by a bracket on each side and the electronics mounting structure. However, standard PLA plastic was too flexible even with a high infill. To increase rigidity, I printed the frame out of a chopped carbon fiber and PLA blend. This provides the rigidity necessary in the drone arms while keeping the overall weight of the frame relatively low. 

<p align="center"><img src="https://github.com/balianirudh/jetson-drone/blob/master/images/testFrame.jpg" width="400" height="300"/><img src="https://github.com/balianirudh/jetson-drone/blob/master/images/droneView1.jpg" width="400" height="300"/></p>
<p align="center">Test 3D print of frame using standard PLA (left), final drone assembly with chopped carbon fiber PLA frame (right)</p>

## Propulsion
