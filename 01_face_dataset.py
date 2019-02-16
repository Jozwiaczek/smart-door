# Imports
import cv2
import os
import sys   
from time import *

# Configuration
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Starting info
current_file_name =  os.path.basename(sys.argv[0])
print("\n [INFO] Starting: %s" % (current_file_name))

# Check exist of list user in dataset and print that if true
FileFaceNamePath = os.path.abspath('name_dataset')
ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)
if  ifExistsFileFaceName:
    print("\nList of user in dataset: \n")
    print("ID | NAME")
    faceNameFileRead = open(FileFaceNamePath,"r")
    if faceNameFileRead.mode == 'r':
        contents = faceNameFileRead.read()
        print(contents)
        
        # Searching of new face ID
        faceNameFileRead.seek(0)
        max = 0
        for line in faceNameFileRead.readlines() :
            num = int(line.split("|")[0])
            if max < num :
                max = num
        face_id = max+1
        faceNameFileRead.close()
else:
    print("\n [INFO] Initializing a file with a list of users")
    face_id = 1

# Main user inputs(NAME, NUMBER OF SAMPLES)
def validation_name (input_name):
    if ifExistsFileFaceName :
        faceNameFileRead = open(FileFaceNamePath,"r")
        faceNameFileRead.seek(0)
        if faceNameFileRead.mode == 'r':
            for line in faceNameFileRead :
                if input_name.lower() in line.lower() :
                    return False
                    faceNameFileRead.close()
    return True                
    

face_name = input('\n Insert the user NAME and press <enter> ==>  ')
while not validation_name(face_name):
    print ("\n That NAME already exists")
    face_name = input('\n Insert another user NAME and press <enter> ==>  ')
        
face_sample_string = input('\n Insert the number of face samples to be taken and press <enter> ==> ')
face_sample_int = int(face_sample_string)
    
def addUser () :
    faceNameFileWrite = open("name_dataset","a+") 
    faceNameFileWrite.write("{}  | {}\r\n".format(face_id ,face_name))
    faceNameFileWrite.close()
    
# Initialize individual sampling face count
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# Timer counting down the time to start taking pictures
for x in range(0,5):
    y = 5-x
    print(y)
    sleep(1)
    
count = 0 #TODO: zrobić możliwość dodawnaia zdjęć a nie zastąpywania
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    photosLeftNumber=face_sample_int-count
    print("Photos left: %d"%(photosLeftNumber)) 
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        #TODO: tworzenie folderu gdy go nie ma
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        print("Face capture interrupted")
        addUser()
        break
    elif count >= face_sample_int: # Take X face sample and stop video
         print("Completed")
         addUser()
         break
        
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
