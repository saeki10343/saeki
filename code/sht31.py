# _*_ coding: utf-8 _*_
import smbus
from time import sleep
import pyfiap
import datetime
import math

# i2cのアドレス
i2c_addr = 0x45
# SMBusモジュールの設定
bus = smbus.SMBus(2)

# SHT31(温湿度センサ)の測定
def SHT31():
    bus.write_byte_data(i2c_addr, 0xE0, 0x00)
    data = bus.read_i2c_block_data(i2c_addr, 0x00, 6)

    # 温度計算
    temp_mlsb = ((data[0] << 8) | data[1])
    temp = -45 + 175 * int(str(temp_mlsb), 10) / (pow(2, 16) - 1)

    # 湿度計算
    humi_mlsb = ((data[3] << 8) | data[4])
    humi = 100 * int(str(humi_mlsb), 10) / (pow(2, 16) - 1)
    return [temp, humi]


def temp2svp( temp ):
    temp = temp+273.15
    a = -6096.9385 / temp
    b = 21.2409642
    c = -2.711193 / 100 * temp
    d = 1.673952 / 100000 * temp * temp
    e = 2.433502 * math.log(temp)
    return( math.exp( a + b + c + d + e ) )

def calc_vpd( temp, humi ):
    svp = temp2svp(temp)   # Saturated Vapour Pressure [Pa]
    vp  = svp * humi / 100 # Vapour Pressure [Pa]
    vpd = (svp-vp)/1000    # Vapour Pressure Dificit [kPa]
    return(vpd)

# i2c通信の設定
bus.write_byte_data(i2c_addr, 0x21, 0x30)
sleep(1)

data = SHT31()
temp = data[0]
humi = data[1]
vpd = calc_vpd(temp, humi)
print( str('{:.4g}'.format(data[0])) + "C" )
print( str('{:.4g}'.format(data[1])) + "%" )
print( str('{:.4g}'.format(vpd)) + "kPa")
print("------")
today = datetime.datetime.now()
fiap = pyfiap.fiap.APP("http://iot.info.nara-k.ac.jp/axis2/services/FIAPStorage?wsdl")
fiap.write([['http://saeki.iwalab/bbg/temperature', "{:.2f}".format(data[0]), today],
            ['http://saeki.iwalab/bbg/humidity', "{:.2f}".format(data[1]), today],
            ['http://saeki.iwalab/bbg/vpd', "{:.4f}".format(vpd), today]])
#ポインタは適宜変更