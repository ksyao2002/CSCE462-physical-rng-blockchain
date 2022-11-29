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
# import blockchain
from ecdsa import SigningKey, VerifyingKey,NIST384p
import pickle

f = open('pk','rb')

# sk = SigningKey.from_der(pickle.load(f))
# f.close()

# my_chain = blockchain.Blockchain()

mining = False
DIFFICULTY = 10

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
while counter<256:
    tmp = [digit for digit in '{0:10b}'.format(chan0.value >>6)]
    numZeros = 0
    for i in range(len(tmp)):
        if tmp[i] == ' ':
            tmp[i] = '0'
        if tmp[i] == '0':
            numZeros +=1

    if numZeros == 10:
        continue
    
    if mining: 
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
            # my_chain.mine(sk)
            # print("New blockchain:")
            # print(my_chain)
            numZerosConsecutive = 0
        if counter%2 ==1:
            ret = [[] for i in range(10)]
    else:
        print(tmp)
        for i in range(len(tmp)):
            ret[i].append(tmp[i])
    #print(chan0.voltage)
    counter+=1
    sleep(0.05)


if mining:
    print()
for i in range(10):
    print(str(i)+": "+"".join(ret[i]))
