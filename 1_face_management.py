# Imports
import cv2
import os
import sys
import RPi.GPIO as GPIO
import numpy as np
from PIL import Image
from time import *
import threading
from progress.bar import *

pinBeep=17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def beep(counter):
  GPIO.setup(pinBeep, GPIO.OUT)
  GPIO.output(pinBeep, GPIO.LOW)
  sleep(counter)
  GPIO.output(pinBeep, GPIO.HIGH)
  GPIO.setup(pinBeep,GPIO.IN)
  
def beeping():
    beep(0.1)
    sleep(0.1)
    beep(0.1)

# Configuration
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Checking exists of directory 'trainer' and create that if not exists
dirTrainerPath = os.path.abspath('trainer')
ifExistsDirTrainer = os.path.isdir(dirTrainerPath)
if not ifExistsDirTrainer :
    os.mkdir(dirTrainerPath)
    print("\n [INFO] Create new directory 'trainer'")

FileFaceNamePath = os.path.abspath('name_dataset')
ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)

# Checking exists of directory 'dataset'
dirDatasetPath = os.path.abspath('dataset')
ifExistsDirDataset = os.path.isdir(dirDatasetPath)
if not ifExistsDirDataset :
    os.mkdir(dirDatasetPath)
    print("Create new directory 'dataset'")

# Check exist of list user in dataset and print that if true
def listOfUser() :
    FileFaceNamePath = os.path.abspath('name_dataset')
    ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)
    numberPhoto = 0  
    
    if  ifExistsFileFaceName:
        print("\nUsers list in dataset:")
        print("ID| NAME | NUMBER OF PHOTOS")
        max = 0
        faceNameFileRead = open(FileFaceNamePath,"r")
        if faceNameFileRead.mode == 'r':
            line = faceNameFileRead.readline()
            if line == "":
                print("      -NO USERS-")
            while line:
                # Get ID from users list
                num = int(line.split("|")[0])
                
                # Get number of photos for ID
                numberPhoto = 0
                for fname in os.listdir("dataset"):
                    if fname.startswith("User.%s"%num):
                        numberPhoto += 1
                        
                # Printing list
                print("{} | {}".format(line.rstrip(), numberPhoto))
                
                # Searching of new face ID
                if max < num :
                    max = num
                line=faceNameFileRead.readline()
             
            faceNameFileRead.close()
            face_id = max+1
            
            #faceNameFileRead.seek(0)
            
    else:
        print("\nInitializing a file with a list of users")
        face_id = 1

def newId():
    if  ifExistsFileFaceName:
        faceNameFileRead = open(FileFaceNamePath,"r")
        if faceNameFileRead.mode == 'r':
            # Searching of new face ID
            faceNameFileRead.seek(0)
            max = 0
            for line in faceNameFileRead.readlines() :
                num = int(line.split("|")[0])
                if max < num :
                    max = num
            faceNameFileRead.close()
            return max+1
    else:
        return 1

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

def addUser (face_name) :
    faceNameFileWrite = open("name_dataset","a+") 
    faceNameFileWrite.write("{} | {}\r\n".format(newId(), face_name))
    faceNameFileWrite.close()
    
def training () :   
    #Check if is any user in users list
    sumUser = 0
    for fname in os.listdir("dataset"):
        sumUser += 1
    
    if sumUser>0:
        def loader():
            # Get number of photos for ID
            numberAllPhoto = 0
            for fname in os.listdir("dataset"):
                numberAllPhoto += 1
                    
            timeToLoad = int(numberAllPhoto/8.6)
            bar = FillingSquaresBar(' Training faces', max=timeToLoad,suffix='%(percent)d%%')
            for i in range(timeToLoad):
                sleep(1)
                bar.next()
            bar.finish()
        
        def trainingFunThread():
            # Path for face image database
            path = 'dataset'
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

            # function to get the images and label data
            def getImagesAndLabels(path):
                imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
                faceSamples=[]
                ids = []
                for imagePath in imagePaths:
                    PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                    img_numpy = np.array(PIL_img,'uint8')
                    id = int(os.path.split(imagePath)[-1].split(".")[1])
                    faces = detector.detectMultiScale(img_numpy)
                    for (x,y,w,h) in faces:
                        faceSamples.append(img_numpy[y:y+h,x:x+w])
                        ids.append(id)
                return faceSamples,ids
            faces,ids = getImagesAndLabels(path)
            recognizer.train(faces, np.array(ids))
            # Save the model into trainer/trainer.yml
            recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
            # Print the numer of faces trained and end program
            print("\n {0} user trained.".format(len(np.unique(ids))))
        
        t1=threading.Thread(target=trainingFunThread,args=())
        t2=threading.Thread(target=loader,args=())
        print("\n")
        t1.start()
        t2.start()
        t1.join()
        
    else:
        print("\n There are no users to train")
    
def wantTraining():
    choiceTraining = input('\n Run trainer? [Y]es  [N]o  ==>  ')
    if choiceTraining.upper() == 'Y':
        training()

def deleteUser():
    listOfUser()
    userToDelete = input('\n Insert ID of user to delete and press <enter> ==>  ')
    
    #Remove user from list
    f = open(os.path.abspath('name_dataset'),"r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if userToDelete not in i:
            f.write(i)
    f.truncate()
    f.close()
    
    #Check if user with that ID exists
    sum = 0
    for fname in os.listdir("dataset"):
        if fname.startswith("User.%s"%userToDelete):
            sum += 1
    
    #Remove face samples of user
    for fname in os.listdir("dataset"):
        if fname.startswith("User.%s"%userToDelete):
            os.remove(os.path.join("dataset",fname))
    
    sumAfterDelete = 0
    for fname in os.listdir("dataset"):
        sumAfterDelete += 1
        
    ifExistsFileTrainer = os.path.isfile("trainer/trainer.yml")
   
    if not sum==0:
        print(" Succesfull remove user with ID = %s"%userToDelete)
        if not sumAfterDelete==0:
            wantTraining()
        elif not ifExistsFileTrainer:
            print(" No users")
        else:
            os.remove("trainer/trainer.yml")
            print(" No users. Remove file <trainer.yml>")
    else:
        print(" \nError. There is no user with ID: %s"%userToDelete)
    
    
    
def addSamples():
    
    #Check if are any photos
    sumAllPhotos = 0
    for fname in os.listdir("dataset"):
        sumAllPhotos += 1
    
    if sumAllPhotos > 0:
        listOfUser()
        userID = input('\n Insert ID of user to add samples and press <enter> ==>  ')
        
        #Check if user with that ID exists
        sumAddSamples = 0
        for fname in os.listdir("dataset"):
            if fname.startswith("User.%s"%userID):
                sumAddSamples += 1
                
        if sumAddSamples > 0:
            face_sample_string = input('\n Insert the number of face samples to be taken and press <enter> ==> ')
            face_sample_int = int(face_sample_string)
            
            # Initialize individual sampling face count
            print("\n Initializing face capture. Look the camera and wait ...")
             
            count = 0
            for fname in os.listdir("dataset"):
                if fname.startswith("User.%s"%userID):
                    count += 1
            counter = 0
            isFirst = True
            isDetect = False
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                
                # Waiting if face is no detect or printing number of photos left
                if len(faces)==0 and isDetect == False:
                    print(" No face detected. Stand in front of the camera.")
                    isDetect = True
                    if not isFirst:
                        beeping()
                elif len(faces)>0:
                    photosLeftNumber=face_sample_int-counter
                    print(" Photos left: %d"%(photosLeftNumber))
                    isDetect = False
                    isFirst = False
                    
                for (x,y,w,h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                    count += 1
                    counter += 1
                    # Save the captured image into the datasets folder
                    cv2.imwrite("dataset/User." + str(userID) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('image', img)
                k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                    cv2.destroyAllWindows()
                    if counter >= 1:
                        beep(1)
                        print(" Face capture interrupted\n Succesfull adding {} face samples".format(face_sample_int)) 
                        wantTraining()
                    break
                elif counter >= face_sample_int: # Take X face sample and stop video
                    beep(1)
                    cv2.destroyAllWindows()
                    print(" \n Succesfull adding {} face samples".format(face_sample_int)) 
                    wantTraining()
                    break
        else:
            print("\n There is no user with this ID: %s"%userID)
    else:
        print("\n There is no any user")
        
def addingUser():
    face_name = input('\n Insert the user NAME and press <enter> ==>  ')
    while not validation_name(face_name):
        print ("\n That NAME already exists")
        face_name = input('\n Insert another user NAME and press <enter> ==>  ')
            
    face_sample_string = input('\n Insert the number of face samples to be taken and press <enter> ==> ')
    face_sample_int = int(face_sample_string)
    
    # Initialize individual sampling face count
    print("\n Initializing face capture. Look the camera and wait ...")
     
    count = 0
    isDetect = False
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        # Waiting if face is no detect or printing number of photos left
        if len(faces)==0 and isDetect == False:
            print(" No face detected. Stand in front of the camera.")
            isDetect = True
            beeping()
        elif len(faces)>0:
            photosLeftNumber=face_sample_int-count
            print(" Photos left: %d"%(photosLeftNumber))
            isDetect = False
            
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(newId()) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            cv2.destroyAllWindows()
            if counter >= 1:
                beep(1)
                addUser(face_name)
                print(" Face capture interrupted\n Succesfull adding {} face samples".format(face_sample_int)) 
                wantTraining()
            break
        elif count == face_sample_int: # Take X face sample and stop video
            beep(1)
            cv2.destroyAllWindows()
            addUser(face_name)
            print(" \n Succesfull adding {} face samples".format(face_sample_int)) 
            wantTraining()
            break


while (True) :
    print ("MENU\n[1] Add user\n[2] Add sample for user\n[3] Delete user\n[4] Show list of users\n[5] Run trainer\n[6] Quit program")
    choice = int(input('Choose action and press <enter> ==>  '))

    #add user
    if choice == 1 :    
        addingUser()
    
    #add sample    
    if choice == 2 :
        addSamples()
            
    #Delete user    
    if choice == 3 :
        deleteUser()
        
    #show list of user    
    if choice == 4 :
        listOfUser()
        
    #Training program
    if choice == 5 :
        training()
        
    #Quit program    
    if choice == 6 :
        print("\nEXITING PROGRAM")
        cam.release()
        break
    
    print ("\n\n================\n")
