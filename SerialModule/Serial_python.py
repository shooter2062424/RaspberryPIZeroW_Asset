# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 20:35:58 2018

@author: shooter
"""

import serial
import time

class Serial:
    portNum = 'COM1'
    serialHandle = None
    
    @staticmethod
    def begin(speed, port=portNum):
        if Serial.serialHandle is not None:
            Serial.serialHandle.close()
        if port is not Serial.portNum:
            Serial.portNum = port
        Serial.serialHandle = serial.Serial(port=port, baudrate=speed, bytesize=serial.EIGHTBITS)
        if not Serial.serialHandle.is_open:
            print("Serial cannot be opened")
        else:
            print("Serial opened, establishing communication on " + Serial.portNum)
        
    @staticmethod
    def end():
        Serial.serialHandle.close()
        Serial.serialHandle = None
        print("Serial closed")
        
    @staticmethod    
    def print(msg):
        if Serial.serialHandle.is_open:
            Serial.serialHandle.write(msg.encode('ascii'))
        else:
            print("Serial encounters unexpected failure")
            Serial.end()
    
    @staticmethod        
    def println(msg):
        if Serial.serialHandle.is_open:
            Serial.serialHandle.write(msg.encode('ascii') + b'\n')
        else:
            print("Serial encounters unexpected failure")
            Serial.end()
            
    @staticmethod
    def available():
        if Serial.serialHandle.is_open:
            return Serial.serialHandle.in_waiting
        else:
            print("Serial is currently not available")
            return 0
        
    @staticmethod
    def read():
        if Serial.serialHandle.is_open:
            return Serial.serialHandle.read()
        else:
            print("Serial is currently not available: failed to read")
            return ""
    
    @staticmethod
    def readln():
        if Serial.serialHandle.is_open:
            s = Serial.serialHandle.readline().decode('ascii').replace('\r\n', '')
            return s
        else:
            print("Serial is currently not available: failed to read line")
            return ""        
            
    
if __name__ == "__main__":
    Serial.begin(9600, 'COM3')
    print("begin")
    time.sleep(5)
    print("delay 5 sec")
    while True:
        d = input("Enter a word: ")
        if d is not 'q':
            Serial.println(d)
            print(Serial.readln())
        else:
            break;
    Serial.end()
            
        