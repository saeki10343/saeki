# -*- coding: utf-8 -*-
from ina219 import INA219 #sudo pip3 install pi-ina219
import time
import pyfiap
import datetime

SHUNT_OHMS = 0.1

ina = INA219(SHUNT_OHMS, address=0x40) # I2Cアドレスを40に指定して、inaのインス
ina.configure() # INA219の初期化
i = 0
totalC = 0
avgC = 0

while i < 9:
        totalC += ina.current()
        # print("Bus Voltage: %.3f V" % ina.voltage())
        # print("Bus Current: %.3f mA" % ina.current())
        # print("Power: %.3f mW" % ina.power())
        # print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
        i += 1
        
avgC = totalC / 10

print("total: %.3f mA" % totalC)
print("average: %.3f mA" % avgC)

times = 0

if avgC > 700:
        times = 4
elif avgC > 550:
        times = 3
elif avgC > 350:
        times = 2
elif avgC > 150:
        times = 1

today = datetime.datetime.now()
fiap = pyfiap.fiap.APP("http://iot.info.nara-k.ac.jp/axis2/services/FIAPStorage?wsdl")
fiap.write([['http://saeki.iwalab/bbg/fan_A', "{:.2f}".format(times), today]])
