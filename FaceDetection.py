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
        if useLowPower:
            self.camResX = 320
            self.camRexY = 240
    
    #method
    def DisplayCam(self):
        self.__openCam()
        while self.cam.isOpened():
            ret, frame = self.cam.read()
            cv.imshow("DISPLAY", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.__closeCam()
        cv.destroyAllWindows()
        
        
    
    def DetectFace(self, b_cap=False):
        self.__openCam()
        #optimize speed
        while self.cam.isOpened():
            ret, frame = self.cam.read()
            grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = FaceDetection.haarFile.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80), flags=cv.CASCADE_SCALE_IMAGE)
            
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            cv.imshow('Detection', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.__closeCam()
        cv.destroyAllWindows()
        
    def TrainRecognizer(self):
        pass
        
    def Recognize(self):
        pass
    
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
    handle = FaceDetection(0)
    print("firstHandle")
    handle = FaceDetection(0)
    print("SecondHandle")
    handle.DetectFace()
    