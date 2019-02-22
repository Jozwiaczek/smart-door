import cv2
import numpy as np
import RPi.GPIO as GPIO
import os
import sys
import threading
from time import *
from lcd import *
from progress.bar import *

# Declaration of pin
pinGreenLed=5
pinRedLed=4
pinYellowLed=26
pinBeep=17
pinBtn=13
pinMagnes=6
pinSensor=19

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinGreenLed, GPIO.OUT)
GPIO.setup(pinRedLed, GPIO.OUT)
GPIO.setup(pinYellowLed, GPIO.OUT)
GPIO.setup(pinBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinMagnes, GPIO.OUT)
GPIO.setup(pinSensor,GPIO.IN, GPIO.PUD_UP)

def beep(counter):
  GPIO.setup(pinBeep, GPIO.OUT)
  GPIO.output(pinBeep, GPIO.LOW)
  sleep(counter)
  GPIO.output(pinBeep, GPIO.HIGH)
  GPIO.setup(pinBeep,GPIO.IN)

def openDoor(getout,ev=None):
  global lcd
  lcd = LCD()

  # Open door
  lcd.clear()
  GPIO.output(pinRedLed, GPIO.HIGH)
  GPIO.output(pinGreenLed, GPIO.LOW)
  GPIO.output(pinMagnes, GPIO.HIGH)
  beep(0.5)

  for x in range(1,11):
    time = 11-x
    if getout == False :
        lcd.message("Hello: %s\nRemaining: %dsec"%(str(id),time))
    else :
        lcd.message("Open doors\nRemaining: %dsec"%(time))
    sleep(1)
    lcd.clear()

  # Close door
  if(GPIO.input(pinSensor)):
    flaga = True;
    while(GPIO.input(pinSensor)):
     if(flaga):
        GPIO.output(pinYellowLed, GPIO.HIGH)
        lcd.message("CLOSE THE DOOR")
        flaga = False
    GPIO.output(pinYellowLed, GPIO.LOW)
  lcd.clear()
  lcd.message("CLOSED")
  GPIO.output(pinGreenLed, GPIO.HIGH)
  GPIO.output(pinRedLed, GPIO.LOW)
  GPIO.output(pinMagnes, GPIO.LOW)
  beep(0.5)

def loader():
    sizeTrainer = int(os.path.getsize('trainer/trainer.yml')/(1024*1024))
    timeToLoad = int(sizeTrainer/4.3)
    bar = FillingSquaresBar('Starting the system', max=timeToLoad,suffix='%(percent)d%%')
    for i in range(timeToLoad):
        sleep(1)
        bar.next()
    bar.finish()

#=====================
# System starts

recognizer = cv2.face.LBPHFaceRecognizer_create()

def readTrainer():
    recognizer.read('trainer/trainer.yml')
        
t1=threading.Thread(target=readTrainer,args=())
t2=threading.Thread(target=loader,args=())

t1.start()
t2.start()
t1.join()

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
# Initialization of the variable to check the face several times
incToOpen=0
# Iniciate id counter
id = 0
# Names related to id
names = ['None']

# List of avalible users
FileFaceNamePath = os.path.abspath('name_dataset')
ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)
if  ifExistsFileFaceName:
    print("\nList of user in dataset:")
    print("ID| NAME")
    faceNameFileRead = open(FileFaceNamePath,"r")
    if faceNameFileRead.mode == 'r':
        contents = faceNameFileRead.read()
        print(contents)
        
        # Searching of new face ID
        faceNameFileRead.seek(0)
        for line in faceNameFileRead.readlines() :
            name = line.split("|")[1]
            names.append(name.split("\n")[0])
        faceNameFileRead.close()


while True:
    if(GPIO.input(pinBtn)== 0):
        openDoor(True)
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            recognitionPercent=int(100-confidence)
            confidence = "  {0}%".format(round(100 - confidence))
            if(recognitionPercent>60):
                incToOpen+=1
            print("Percentage of recognition: %d"%recognitionPercent)
            print("The flag to open: %d"%incToOpen)
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            incToOpen=0
        if(incToOpen==5):
          openDoor(False)
          incToOpen=0

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

    cv2.imshow('Smart Doors - Monitoring',img) 
    k = cv2.waitKey(10) & 0xff 
    if k == 27: # Press 'ESC' for exit program
        break
    if k == 32: # Press 'Space' to open door
        openDoor(True)
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
GPIO.cleanup()
