# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 21:13:01 2018

@author: shooter
"""
import numpy as np
import cv2 as cv

class FaceDetection:
    #static variables
    usedCamID = []
    camObjPool = []
    haarFile = cv.CascadeClassifier("./haarcascade_frontalface_default.xml")
    lbpFile = cv.CascadeClassifier("./lbpcascade_frontalface_improved.xml")
    i_trainNeedDataNum = 4
    face_recognizer = cv.face.LBPHFaceRecognizer_create() 
    
    def __new__(cls, camID):
        if camID not in FaceDetection.usedCamID:
            newCam = object.__new__(cls)
            FaceDetection.usedCamID.append(camID)
            FaceDetection.camObjPool.append(newCam)
            return newCam
        else:
            print("Warning, same camID is already used!")
            idx = FaceDetection.usedCamID.index(camID)
            return FaceDetection.camObjPool[idx]        
    
    #constructor
    def __init__(self, camID, useLowPower=True):
        self.cam = None
        self.camID = camID
        self.camResX = 640
        self.camResY = 480
        self.waitTime = 25
        self.minSize = 80
        self.b_showVideo = True
        if useLowPower:
            self.camResX = 320
            self.camRexY = 240
            self.waitTime = 40
            self.minSize = 20
            self.b_showVideo = False
    
    #method
    def DisplayCam(self):
        if not self.b_showVideo:
            print('The imshow has been disabled!')
            return
        
        self.__openCam()
        while self.cam.isOpened():
            ret, frame = self.cam.read()
            cv.imshow("DISPLAY", frame)
            if (cv.waitKey(self.waitTime) & 0xFF) == ord('q'):
                break
        self.__closeCam()
        cv.destroyAllWindows()
        
        
    
    def DetectFace(self, b_record4train=False, b_useLBP=True, b_debug=False):
        self.__openCam()
        if not b_record4train:  #normal face detection
            while self.cam.isOpened():
                ret, frame = self.cam.read()
                grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
                if not b_useLBP:
                    faces = FaceDetection.haarFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)
                else:
                    faces = FaceDetection.lbpFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)
            
                if self.b_showVideo or b_debug:
                    for (x, y, w, h) in faces:
                        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                    cv.imshow('Detection', frame)
                else:
                    print('Face Detected: ', len(faces))

                if (cv.waitKey(self.waitTime) & 0xFF) == ord('q'):
                    break
            self.__closeCam()
            cv.destroyAllWindows()    
            return [], 1
        else:
            faceCount = 0
            datas = []
            while faceCount < FaceDetection.i_trainNeedDataNum:
                ret, frame = self.cam.read()
                grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
                if not b_useLBP:
                    faces = FaceDetection.haarFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)
                else:
                    faces = FaceDetection.lbpFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)

                if len(faces) is not 0:
                    faces = faces.tolist()
                    faces.sort(key=lambda x: x[2]*x[3])
                    #choose the biggest one
                    bFace = faces[-1]
                    datas.append(grayImg[bFace[1]:bFace[1]+bFace[3], bFace[0]:bFace[0]+bFace[2]])
                    faceCount = faceCount + 1
            self.__closeCam()  
            return datas, 1              
        
    def TrainRecognizer(self, faces, labels):
        FaceDetection.face_recognizer.train(faces, labels)
        
    def Recognize(self, b_useLBP=True, b_debug=False):
        self.__openCam()
        while self.cam.isOpened():
            ret, frame = self.cam.read()
            grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            if not b_useLBP:
                faces = FaceDetection.haarFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)
            else:
                faces = FaceDetection.lbpFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(self.minSize, self.minSize), flags=cv.CASCADE_SCALE_IMAGE)
            
            if self.b_showVideo or b_debug:
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if len(faces) is not 0:
                    faces = faces.tolist()
                    faces.sort(key=lambda x: x[2]*x[3])
                    #choose the biggest one
                    bFace = faces[-1]
                    face = grayImg[bFace[1]:bFace[1]+bFace[3], bFace[0]:bFace[0]+bFace[2]]
                    label = FaceDetection.face_recognizer.predict(face)
                    print(label)
                cv.imshow('Detection', frame)
            else:
                print('Face Detected: ', len(faces))

            if (cv.waitKey(self.waitTime) & 0xFF) == ord('q'):
                break
        self.__closeCam()
        cv.destroyAllWindows()            
        
    
    def __openCam(self):
        if self.cam == None:
            self.cam = cv.VideoCapture(self.camID)
            self.cam.set(cv.CAP_PROP_FRAME_WIDTH, self.camResX)
            self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.camResY)
    
    def __closeCam(self):
        if self.cam != None:
            self.cam.release()
            self.cam = None

if __name__ == "__main__":
    #detect face
    handle = FaceDetection(0)
    handle.DetectFace(b_record4train=False, b_useLBP=True, b_debug=True)
    
    #face recognition
    data, label = handle.DetectFace(b_record4train=True, b_useLBP=True)
    handle.TrainRecognizer(data, np.array([label]*len(data)))
    handle.Recognize(b_debug=True)
    
    
    
