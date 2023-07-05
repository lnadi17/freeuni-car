# freeuni-car
This project, also known as "Freecar", was initially developed as a Sophomore Project at Free University of Tbilisi. 
The aim was to create a remote controlled toy car using a Raspberry Pi, 
which could be controlled via a web interface and would have various fun features.
It was a complex project where we all learned much about engineering. 
Currently, this repository is archived and the hardware of the car itself is disassembled, only the early prototype videos and pictures are displayed here.

<figure>
  <img src="./readme_images/early_demo.gif" alt="Early Prototype">
  <figcaption>Early prototype showcase of the project</figcaption>
</figure>

## Features
- The car hosted a web server and allowed users to connect to it through Campus Wi-Fi. The web interface displayed a live stream from the car's camera and provided WASD controls for movement. 
- Using the SHIFT key increased the engine power to 100%. 
- The project also utilized OpenCV library for environment analysis, including brightness detection and automatic activation of LED headlights in low-light conditions.
- As a safety mechanism, an ultrasonic sensor was attached to the bottom of the car, preventing it from being pushed off high obstacles 
such as tables and stairs.
- The car had the ability to display its current location across the University Campus, based on the strength of Wi-Fi signals.
  This was possible thanks to [FIND Framework](https://github.com/schollz/find).
- Remaining capacity of rechargable Li-ion batteries was displayed on the screen.
- Many other misc features were available, such as taking a screenshot, showing a black and white image, etc.
- An unfinished feature was auto-navigation and finding a charging station when the battery was low.

## 
