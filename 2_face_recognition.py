import cv2
import numpy as np
import RPi.GPIO as GPIO
import os
import sys
from time import *
from lcd import *

# Starting info
current_file_name =  os.path.basename(sys.argv[0])
print("\nStarting: %s" % (current_file_name))

# Declaration of pin
pinGreenLed=5
pinRedLed=4
pinBeep=17
pinBtn=13
pinMagnes=6
pinSensor=19

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinGreenLed, GPIO.OUT)
GPIO.setup(pinRedLed, GPIO.OUT)
GPIO.setup(pinBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinMagnes, GPIO.OUT)
GPIO.setup(pinSensor,GPIO.IN, GPIO.PUD_UP)

def beep(counter):
  GPIO.setup(pinBeep, GPIO.OUT)
  GPIO.output(pinBeep, GPIO.LOW)
  sleep(counter)
  GPIO.output(pinBeep, GPIO.HIGH)
  GPIO.setup(pinBeep,GPIO.IN)

def openDoor(ev=None):
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
    lcd.message("Witaj: %s\nPozostalo: %dsek"%(str(id),time))
    sleep(1)
    lcd.clear()

  # Close door
  if(GPIO.input(pinSensor)):
    flaga = True;
    while(GPIO.input(pinSensor)):
     if(flaga):
       lcd.message("DRZWI SIE ZAMYKA \nTO NIE AFRYKA!!!")
       flaga = False
  lcd.clear()
  lcd.message("ZAMKNIETE")
  GPIO.output(pinGreenLed, GPIO.HIGH)
  GPIO.output(pinRedLed, GPIO.LOW)
  GPIO.output(pinMagnes, GPIO.LOW)
  beep(0.5)

print("Start systemu...")
#=====================
#Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
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
#inicjacja zmiennej do kilkukrotnego sprawdzenia danej twarzy
incToOpen=0
print("Program zaladowany")

#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None']

# List of avalible users
FileFaceNamePath = os.path.abspath('name_dataset')
ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)
if  ifExistsFileFaceName:
    print("\nList of user in dataset:")
    print("ID | NAME")
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
        openDoor()
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
            rozpoznanie=100-confidence
            confidence = "  {0}%".format(round(100 - confidence))
            if(rozpoznanie>30):
            	incToOpen+=1
            print(rozpoznanie)
            print(incToOpen)
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            incToOpen=0
        if(incToOpen==5):
          openDoor()
          incToOpen=0

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

    cv2.imshow('Program do rozpoznawania twarzy',img) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
GPIO.cleanup()
