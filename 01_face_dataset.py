import cv2
import os
from time import *
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# For each person, enter one numeric face id
face_id = input('\n Wpisz ID uzytkownika i przycisnij <enter> ==>  ')
face_sample_string = input('\n Wpisz liczbe probek twarzy do wykonania i przycisnij <enter> ==> ')
face_sample_int=int(face_sample_string)
# Initialize individual sampling face count
count = 0
for x in range(1,4):
    y = 4-x
    print(y)
    sleep(1)
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    iloscZdjec=face_sample_int-count
    print("Jeszcze: %d zdjec"%(iloscZdjec)) 
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        print("Zakonczono")
        break
    elif count >= face_sample_int: # Take 30 face sample and stop video
         print("Zakonczono")
         break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
