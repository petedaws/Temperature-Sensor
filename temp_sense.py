#! /usr/bin/python

import serial


serialport = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
while(True):
        response = serialport.readlines(None)
        print response
