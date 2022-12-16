#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics
###imports for TTN connection
from network import LoRa
import network
###imports for main code
import time
import pycom
from pycoproc_1 import Pycoproc
import machine
import socket
import ubinascii
import array
###import of libraries for each sensor
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
###
pycom.heartbeat(False)


py = Pycoproc(Pycoproc.PYSENSE)

lora = LoRa(mode = LoRa.LORAWAN)

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('AED547666A2978DD169E15194F1117F3')
dev_eui = ubinascii.unhexlify('70B3D57ED0049E64')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')

# alt = MPL3115A2(py, mode=ALTITUDE)
    # alt0 = int(alt.altitude())

while(True):

    #Get the pressure data and convert to protocol (pressure = (bytes[0]/2)+950)
    press = MPL3115A2(py, mode=PRESSURE)
    press0 = press.pressure() / 100
    press0 -= 950
    press0 *= 2
    press0 = int(press0)


    # add red light and blue light together.
    lit = LTR329ALS01(py)
    lit0 = lit.light()
    lightCombined = lit0[0] + lit0[1]


    #temperature = ((bytes[2]-20)*10 + bytes[3])/10
    temp = SI7006A20(py).temperature()
    #INTEGER PART (add 20 so that negative values can be send to the network according to protcol)
    tempInt = int(temp)
    #DECMIAL PART
    tempDecimal = int((temp-tempInt) * 100)

    dataArray = [0] * 3

    #print("Altitude: " + str(alt0))
    print("Pressure: " + str(press0))
    print("Light: " + str(lit0))
    print("temp: " + str(temp))
    print("Temperature: " + str(tempInt) + "." + str(tempDecimal))

    if lightCombined > 255:
        lightCombined = 255
    elif lightCombined < 0:
        lightCombined = 0

    if press0 > 255:
        press0 = 255
    elif press0 < 0:
        press0 = 0

    #if temp0 > 255:
    #    temp0 = 255
    #elif temp0 < 0:
    #    temp0 = 0

    dataArray[0] = int(press0)
    dataArray[1] = int(lightCombined)
    dataArray[2] = int((lit0[0] + lit0[1])/2)
    dataArray[2] = int(tempInt) - 10

    print(dataArray)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    s.setblocking(True)

    s.send(bytes([dataArray[0], dataArray[1], dataArray[2]]))

    s.setblocking(False)

data = s.recv(128)
print(data)
time.sleep(500)
