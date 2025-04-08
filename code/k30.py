#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python app to run a K-30 Sensor
import serial
import time
import pyfiap
import datetime

ser = serial.Serial("/dev/ttyO2",baudrate=9600,timeout=0.5)#シリアルは適宜変更
ser.flushInput()
time.sleep(1)
#strData = "\xFE\x44\x00\x08\x02\x9F\x25"

while True:
        #ser.write(strData.encode())
        ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
        time.sleep(.1)
        resp = ser.read(7)
        co2 = 0
        if resp==b'':
         print("wait")
        else:
         high = resp[3]
         low = resp[4]
         co2 = (high*256) + low
         print ("Co2 = " + str(co2) + "ppm")
         if co2 != 0:
          if co2 < 5000:
           break
         #time.sleep(3)

today = datetime.datetime.now()
fiap = pyfiap.fiap.APP("http://iot.info.nara-k.ac.jp/axis2/services/FIAPStorage?wsdl")
fiap.write(['http://saeki.iwalab/bbg/co2_k30', "{:.2f}".format(co2), today])