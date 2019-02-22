# Smart-Doors v1.0
Smart door opening via Raspberry Pi using face recognition.

![enter image description here](https://lh3.googleusercontent.com/ZuzLBom_JPEEM14VQioGLCJJWu3Mqh9_ecLV-SS9GiK_wT2KnzoZeclkjZpW9ACmv5bqXqTs220x=s220)

## Overview:
This project provides software and hardware installation instructions for smart doors. The software is designed to run on a Raspberry Pi, which is an inexpensive ARM-based computer.

## Requirements:

 - [Raspberry Pi](http://www.raspberrypi.org/) (In my case it is Raspberry Pi B+)
 - Micro USB charger (1.5A preferable) for power supply your Raspberry Pi
 - Micro SD Card
 - [Starter Kit V3.0 for Raspberry Pi](https://pl.aliexpress.com/item/SunFounder-Super-Starter-Learning-Kit-V3-0-for-Raspberry-Pi-3-2-Model-B-1-Model/32805707137.html?spm=a2g0s.9042311.0.0.27425c0fwNGuQX)
 - [Electro-Magnetic Lock](https://pl.aliexpress.com/item/60KG-132lb-Electric-Magnetic-Lock-Fail-Secure-DC-12V-for-Door-Entry-Access-Control-System/32764160255.html?spm=a2g0s.9042311.0.0.27425c0fcBsA9n)
 - [Raspberry Pi Camera Night Vision](https://pl.aliexpress.com/item/Raspberry-Pi-Camera-RPI-Focal-Adjustable-Night-Version-Camera-Acrylic-Holder-IR-Light-FFC-Cable-for/32796213162.html?spm=a2g0s.9042311.0.0.27425c0fcBsA9n)
 - [Relay 5V 10A/250VAC](https://botland.com.pl/en/relays/8463-relay-5v-10a250vac.html) for lock
 - [Power supply 12V / 1A](https://botland.com.pl/en/mains-power-supplies/5045-power-supply-12v-1a-dc-plug-55-25mm.html) for power supply your lock. 
 The end of the cable is not important because it must be cut off anyway.
 - [Raspberry Pi tape - camera 200cm](https://botland.com.pl/en/ffc-fpc-connectors/3952-raspberry-pi-tape-camera-200cm-15-wires-1mm-raster.html)
 - [Magnetic sensor to open Door](https://botland.com.pl/en/magnetic-sensors/3104-magnetic-sensor-to-open-door-window-reed-contact-cmd14-screws.html)


## Hardware Setup:
![enter image description here](https://lh3.googleusercontent.com/d3fj4aBOaN3fpGIbpKns15QNstFF4ihZ2WMupRjTqvkvAG_EOvPFVuIfbylhvCiZUPf4PFkdKw1T=s400)

*Step 1:*

*Documentation of hardware settings in preparation...*



#### Using the breadboard to connect the pins:
1. Green led = 5
2. Red led = 4
3. Yellow led = 26
4. Buzzer = 17
5. pinBtn = 13
6. LockDoor = 6
7. Sensor of opening door = 19
8. LCD Screen:
	1. D7 = 18
	2. RS = 27
	3. E = 22
	4. D6 = 23
	5. D5 = 24
	6. D4 = 25


## Software Installation:
 1.  Install [Rasbian](https://www.raspberrypi.org/downloads/raspbian/)  onto your Raspberry Pi
 
 2. Activate VNC on Raspberry Pi to operate the device remotely via a computer, not via HDMI [Recommend [RealVNC](https://www.realvnc.com/en/connect/download/viewer/)]
 
 3. Activate the camera on Raspberry Pi in raspi-config [[More info](https://www.raspberrypi.org/documentation/configuration/camera.md)]
 
 4. Install OpenCv 3 [[Tutorial](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)]. 

	> Remember to select Python 3 when configuring your virtual environment

 5. I recommends run the command "source" each time you open up a new terminal to ensure your system variables have been set up correctly.  
  `source ~/.profile`

 6. Next, let's enter on virtual environment: 
 `workon cv`

	> Remember to always work on this project in a virtual environment,
	> otherwise the program will not work without OpenCv


 7. Add camera drivers `bcm2835-v4l2` to the last line by opening file `sudo nano /etc/modules file`

 8. Install PIL library 
 `pip install pillow`

 9. Install module to control [Raspberry Pi GPIO](https://pypi.org/project/RPi.GPIO/) channels
 `pip install RPi.GPIO`
 
 10. Install [progress](https://pypi.org/project/progress/) bar library 
 `pip install progress`
	 
 11. Now you can enjoy with that project :)


## How to use Smart Doors:

### 1. Face Management
1. Run file **1_face_management.py**.  This program allows you to manage a list of users based on which faces are recognized.
2. To perform an action, you must enter the listing number. The menu displays:
![enter image description here](https://lh3.googleusercontent.com/hJ12ZvUku-cmIZDbOpJ36APbwTM7djWu5eCEM5RKxtMmfVPBrqNf37ucKtdHELoCA3dJQoHgqEzu)
	- **Add user**: You enter the nickname of the user, the number of samples you want to give him, and then take pictures of the face.
	- **Add sample for user**: This will add the specified number of photos to an existing user.
	- **Delete user**: This can remove a specific user from your list.
	- **Show list of users**: This shows id, nicknames and the number of samples for each user
	- **Run trainer**: Every time you want your changes (adding a user, adding samples or deleting a user) to be taken into account when recognizing faces, you must use a trainer.
	- **Quit program**

	> After each, adding a user or samples or removing a user, the program asks if you want to use a trainer. 
	> If you plan to do several activities, I recommend that you leave it at the very end, because with a large number of samples it takes a while.
		
3. To be able to run FaceRecognizer at all you have to add at least one user and run trainer. I recommend that you add at least 200/300 samples for proper operation.

### 2. Face Recognizer
1. Run **2_face_recognition.py** and enjoy the magic of the smart door 
2. Program w termi
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1NjU4MjU4ODEsLTQ1NDQxOTU3MSwtMT
k3NjM2MjE1NSwtMTI0OTQ4NDkzNCwtNDg4NjM2NzA1LC0xMTcy
NTE1ODkyLDkyNDIzOTY4LC0xMjk1NDAyMzc5LC04NTM1NDY2Ni
wtOTcwMzkxOTk1LC0zMzQ3MzM0MTcsMTYzODM4MDY5MiwtOTQw
ODQ5NDY4LC0yNzI5NDUwMjQsMTc0NzM1MjkxOF19
-->