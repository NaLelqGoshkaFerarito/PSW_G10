from machine import UART
import machine
import os

uart = UART(0, 115200)
os.dupterm(uart)

machine.main('main.py')
