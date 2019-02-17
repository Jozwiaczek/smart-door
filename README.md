# Smart-Doors v1.0
Smart door opening via Raspberry Pi using face recognition.

![enter image description here](https://lh3.googleusercontent.com/ZuzLBom_JPEEM14VQioGLCJJWu3Mqh9_ecLV-SS9GiK_wT2KnzoZeclkjZpW9ACmv5bqXqTs220x=s220)

## Overview:
This project provides software and hardware installation instructions for smart doors. The software is designed to run on a Raspberry Pi, which is an inexpensive ARM-based computer.

## Requirements:

#### Hardware
 - [Raspberry Pi](http://www.raspberrypi.org/) (In my case it is Raspberry Pi B+)
 - Micro USB charger (1.5A preferable)
 - micro SD Card
 - [Magnetic Contact Switch](http://amzn.com/B006VK6YLC)
 - [Zestaw KIT](https://pl.aliexpress.com/item/SunFounder-Super-Starter-Learning-Kit-V3-0-for-Raspberry-Pi-3-2-Model-B-1-Model/32805707137.html?spm=a2g0s.9042311.0.0.27425c0fwNGuQX)
 - [Zamek Elektro-Magnetyczny](https://pl.aliexpress.com/item/60KG-132lb-Electric-Magnetic-Lock-Fail-Secure-DC-12V-for-Door-Entry-Access-Control-System/32764160255.html?spm=a2g0s.9042311.0.0.27425c0fcBsA9n)
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

#### Używając breadboard podłączenie pinów:
1. Zielona dioda led = 5
2. Czerwona dioda led = 4
3. Buzzer = 17
4. pinBtn = 13
5. Elektromages = 6
6. Sensor otwarecia drzwi = 19
7. Ekran LCD:
	1. D7 = 18
	2. RS = 27
	3. E = 22
	4. D6 = 23
	5. D5 = 24
	6. D4 = 25


## Software Installation:
1.  **Install [Rasbian](https://www.raspberrypi.org/downloads/raspbian/)  onto your Raspberry Pi**
2. Aktywuj VNC na Raspberry Pi by obsługiwać urządzenie zdalnie, a nie przez HDMI
3. Ściągnij ,zainstaluj oraz połącz Raspberry Pi ze swoim komputerem poprzez program VNC (zalecam [RealVNC](https://www.realvnc.com/en/connect/download/viewer/))
4. Uruchom kamerę na Raspberry Pi w raspi-config


## TODO:
This section contains the features I would like to add to the application, but do not currently have time for. If someone would like to contribute changes or patches, I would be all to happy to incorporate them.


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5Mzc3MDI5OTUsLTMzNDczMzQxNywxNj
M4MzgwNjkyLC05NDA4NDk0NjgsLTI3Mjk0NTAyNCwxNzQ3MzUy
OTE4XX0=
-->