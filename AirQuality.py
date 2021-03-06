#!/usr/bin/python3
#-*- coding:utf-8 -*-

import serial

class AirQuality(object):
    """Air Quality"""
    def __init__(self):
        self.ser = serial.Serial(
        	port='/dev/ttyAMA0',              # number of device, numbering starts at
        	baudrate=9600,          # baud rate
        	bytesize=serial.EIGHTBITS,     # number of databits
        	parity=serial.PARITY_NONE,     # enable parity checking
        	stopbits=serial.STOPBITS_ONE,  # number of stopbits
        	timeout=2,           # set a timeout value, None for waiting forever
        	xonxoff=0,              # enable software flow control
        	rtscts=0,               # enable RTS/CTS flow control
	   )

    def _check(self,data):
        #print(data)
        if data[0]!=0xAA:
            return False
        if data[1]!=0xC0:
            return False
        if data[9]!=0xAB:
            return False
        temp=data[2]+data[3]+data[4]+data[5]+data[6]+data[7]
        if temp&0xFF!=data[8]:
            return False
        return True


    def getData(self):
        while self.ser.read(1)!=b'\xaa':
            pass
        s = self.ser.read(9)
        data = [0xAA]
        for i in s:
            data.append(i)
        if self._check(data):
            pm25=(data[2]+data[3]*256)/10
            pm10=(data[4]+data[5]*256)/10
            #print("PM2.5=%.2f, PM10=%.2f" %(pm25, pm10))
        else:
            pm25=pm10=0
        return (pm25,pm10)

    def __exit__(self):
        self.ser.close()
