# Imports
import cv2
import os
import sys   
from time import *


# TODO: GUI

# Configuration
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

FileFaceNamePath = os.path.abspath('name_dataset')
ifExistsFileFaceName = os.path.isfile(FileFaceNamePath)

# Checking exists of directory 'dataset'
dirDatasetPath = os.path.abspath('dataset')
ifExistsDirDataset = os.path.isdir(dirDatasetPath)
if not ifExistsDirDataset :
    os.mkdir(dirDatasetPath)
    print("Create new directory 'dataset'")

# Starting info
current_file_name =  os.path.basename(sys.argv[0])
print("\nStarting: %s" % (current_file_name))

# Check exist of list user in dataset and print that if true
def listOfUser() :
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

def addUser () :
    faceNameFileWrite = open("name_dataset","a+") 
    faceNameFileWrite.write("{} | {}\r\n".format(newId(), face_name))
    faceNameFileWrite.close()
    

while (True) :
    print ("MENU\n[1] Add user\n[2] Add sample for user\n[3] Delete user\n[4] Show list of users\n[5] Quit program")
    choice = int(input('Choose action and press <enter> ==>  '))

    #add user
    if choice == 1 :    
        face_name = input('\n Insert the user NAME and press <enter> ==>  ')
        while not validation_name(face_name):
            print ("\n That NAME already exists")
            face_name = input('\n Insert another user NAME and press <enter> ==>  ')
                
        face_sample_string = input('\n Insert the number of face samples to be taken and press <enter> ==> ')
        face_sample_int = int(face_sample_string)
        
        # Initialize individual sampling face count
        print("\n Initializing face capture. Look the camera and wait ...")

        # Timer counting down the time to start taking pictures
        for x in range(0,4):
            y = 4-x
            print(" %d"%y)
            sleep(1)
         
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
                print(" Face capture interrupted")
                addUser()
                cam.release()
                cv2.destroyAllWindows()
                break
            elif count >= face_sample_int: # Take X face sample and stop video
                print(" \n Succesfull adding user {} with {} face samples".format(face_name,face_sample_int))
                addUser()
                cam.release()
                cv2.destroyAllWindows()
                break
        break
    
    #add sample    
    if choice == 2 :
        listOfUser()
        userID = input('\n Insert ID of user to add samples and press <enter> ==>  ')
        
        face_sample_string = input('\n Insert the number of face samples to be taken and press <enter> ==> ')
        face_sample_int = int(face_sample_string)
        
        # Initialize individual sampling face count
        print("\n Initializing face capture. Look the camera and wait ...")

        # Timer counting down the time to start taking pictures
        for x in range(0,4):
            y = 4-x
            print(" %d"%y)
            sleep(1)
         
        sum = 0
        for fname in os.listdir("dataset"):
            if fname.startswith("User.%s"%userID):
                sum += 1
        count = sum
        counter = 0
        
        isDetect = False
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            # Waiting if face is no detect or printing number of photos left
            if len(faces)==0 and isDetect == False:
                print(" No face detected. Stand in front of the camera.")
                isDetect = True
            elif len(faces)>0:
                photosLeftNumber=face_sample_int-counter
                print(" Photos left: %d"%(photosLeftNumber))
                isDetect = False
                
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                counter += 1
                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(userID) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                print(" Face capture interrupted")
                cam.release()
                cv2.destroyAllWindows()
                break
            elif counter >= face_sample_int: # Take X face sample and stop video
                print(" \n Succesfull adding {} face samples".format(face_sample_int))
                cam.release()
                cv2.destroyAllWindows()
                break
        break
    
    #Delete user    
    if choice == 3 :
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
        
        #Remove face samples of user
        for fname in os.listdir("dataset"):
            if fname.startswith("User.%s"%userToDelete):
                os.remove(os.path.join("dataset",fname))
        
        print(" Succesfull remove user with ID = %s"%userToDelete)
        
    #show list of user    
    if choice == 4 :
        listOfUser()
        
    #Quit program    
    if choice == 5 :
        print("\nExiting Program")
        break
    
    print ("\n\n================\n")
