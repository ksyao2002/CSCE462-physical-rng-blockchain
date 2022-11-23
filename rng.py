# CSCE 462 Lab 3
# Kevin Yao and Omar Irshad
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from time import sleep, clock_gettime
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import busio
import digitalio
import math
import numpy as np
import board

DIFFICULTY = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)

chan0 = AnalogIn(mcp, MCP.P0)

frame = []

start_time = clock_gettime(0)
ret = [[] for i in range(10)]
counter = 0
numZerosConsecutive = 0
while True:
    tmp = [digit for digit in '{0:10b}'.format(chan0.value >>6)]
    numZeros = 0
    for i in range(len(tmp)):
        if tmp[i] == ' ':
            tmp[i] = '0'
        if tmp[i] == '0':
            numZeros +=1

    if numZeros == 10:
        continue
    
    # print(tmp)
    for i in range(len(tmp)):
        ret[i].append(tmp[i])
        if counter%2 == 1:
            if ret[i][0] != ret[i][1]: #removing bias. Don't count if they are the same bit
                print(ret[i][0],end='', flush=True) #continuously print stream of random numbers
                if ret[i][0] == '0':
                    numZerosConsecutive +=1
                else:
                    numZerosConsecutive = 0

    if numZerosConsecutive >= DIFFICULTY:
        print("\n\n ************** BLOCK PRODUCED ************** \n\n")
        numZerosConsecutive = 0
    if counter%2 ==1:
        ret = [[] for i in range(10)]

    #print(chan0.voltage)
    counter+=1
    sleep(0.05)

print()