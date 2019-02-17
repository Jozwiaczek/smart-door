# Smart-Doors v1.0
Smart door opening via Raspberry Pi using face recognition.

![enter image description here](https://lh3.googleusercontent.com/ZuzLBom_JPEEM14VQioGLCJJWu3Mqh9_ecLV-SS9GiK_wT2KnzoZeclkjZpW9ACmv5bqXqTs220x=s220)

## Overview:
This project provides software and hardware installation instructions for smart doors. The software is designed to run on a Raspberry Pi, which is an inexpensive ARM-based computer.

## Requirements:

#### Hardware
 - [Raspberry Pi](http://www.raspberrypi.org/) (In my case it is Raspberry Pi B+)
 - Micro USB charger (1.5A preferable)
 - Micro SD Card
 - [Magnetic Contact Switch](http://amzn.com/B006VK6YLC)
 - [Starter Kit V3.0 for Raspberry Pi](https://pl.aliexpress.com/item/SunFounder-Super-Starter-Learning-Kit-V3-0-for-Raspberry-Pi-3-2-Model-B-1-Model/32805707137.html?spm=a2g0s.9042311.0.0.27425c0fwNGuQX)
 - [Electro-Magnetic Lock](https://pl.aliexpress.com/item/60KG-132lb-Electric-Magnetic-Lock-Fail-Secure-DC-12V-for-Door-Entry-Access-Control-System/32764160255.html?spm=a2g0s.9042311.0.0.27425c0fcBsA9n)
 - [Raspberry Pi Camera Night Vision](https://pl.aliexpress.com/item/Raspberry-Pi-Camera-RPI-Focal-Adjustable-Night-Version-Camera-Acrylic-Holder-IR-Light-FFC-Cable-for/32796213162.html?spm=a2g0s.9042311.0.0.27425c0fcBsA9n)
 - 


#### Software
 - Raspbian
 - Python 3.5
 - OpenCV



## Hardware Setup:
![enter image description here](https://lh3.googleusercontent.com/d3fj4aBOaN3fpGIbpKns15QNstFF4ihZ2WMupRjTqvkvAG_EOvPFVuIfbylhvCiZUPf4PFkdKw1T=s400)

*Step 1:*

Describe

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

 7. Next, let's enter on virtual environment: 
 `workon cv`

	> Remember to always work on this project in a virtual environment,
	> otherwise the program will not work without OpenCv


 7. Add camera drivers `bcm2835-v4l2` to the last line by opening file `sudo nano /etc/modules file`

 8. Install PIL library 
 `pip install pillow`

 9. Install module to control Raspberry Pi GPIO channels
 `pip install RPi.GPIO`
 
 10. Run file **1_face_management.py** and choose *[1] Add user* to add new user with face samples
		![enter image description here](https://lh3.googleusercontent.com/yGJpRubCJUU9t5htu5X2TKgAxZJKJH-S56T07qFlUBnv6hfDlf1-Qh-wVfxqbSVtpnOn6yYsVkfX)

 11. Run again **1_face_management.py** and choose option *[5] Face training* to train a recognaizer. 
	![enter image description here](https://lh3.googleusercontent.com/zlFmj1s6J9vheZ3nLv-1mSn0VQxp8wj23cxZGlDbXf4hv-TfaHZPdvKgLgNuUt4QkgoXyLq5C0LE)

		> Every time you add a new user or you update something, you must repeat this step!

12. Run **2_face_recognition.py** and enjoy the magic of the smart door :)


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExNzI1MTU4OTIsOTI0MjM5NjgsLTEyOT
U0MDIzNzksLTg1MzU0NjY2LC05NzAzOTE5OTUsLTMzNDczMzQx
NywxNjM4MzgwNjkyLC05NDA4NDk0NjgsLTI3Mjk0NTAyNCwxNz
Q3MzUyOTE4XX0=
-->