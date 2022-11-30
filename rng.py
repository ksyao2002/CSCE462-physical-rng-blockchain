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
import blockchain
from ecdsa import SigningKey, VerifyingKey,NIST384p
import pickle
import json

f = open('pk','rb')

sk = SigningKey.from_der(pickle.load(f))
f.close()

my_chain = blockchain.Blockchain()

num_mined = 0

mining = False
printing = False
testing = True
DIFFICULTY = 5

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
numRandomBitsCounter = 0
while True:
    if testing and counter>1024:
        break
    tmp = [digit for digit in '{0:10b}'.format(chan0.value >>6)]
    numZeros = 0
    for i in range(len(tmp)):
        if tmp[i] == ' ':
            tmp[i] = '0'
        if tmp[i] == '0':
            numZeros +=1

    if numZeros == 10:
        print("Skipping since all zero")
        continue
    
    if printing: 
        # print(tmp)
        for i in range(len(tmp)):
            ret[i].append(tmp[i])
            if counter%2 == 1:
                if ret[i][0] != ret[i][1]: #removing bias. Don't count if they are the same bit
                    print(ret[i][0],end='', flush=True) #continuously print stream of random numbers
                    
                    if mining:
                        if numRandomBitsCounter % (DIFFICULTY) == 0:
                            numZerosConsecutive = 0
                        if ret[i][0] == '0': #The first DIFFICULTY number of bits in each 32 bit word must be 0's
                            numZerosConsecutive +=1
                            if numZerosConsecutive >= DIFFICULTY:
                                print("\n\n ************** BLOCK PRODUCED ************** \n\n")
                                my_chain.mine(sk)
                                print("New blockchain:")
                                my_chain.print_chain()
                                numZerosConsecutive = 0
                                num_mined+=1
                        else:
                            numZerosConsecutive = 0
                        numRandomBitsCounter +=1

        
        if counter%2 ==1:
            ret = [[] for i in range(10)]
    else:
        print(tmp)
        for i in range(len(tmp)):
            ret[i].append(tmp[i])
    #print(chan0.voltage)
    counter+=1
    sleep(0.05)

if testing:
    numWords = numRandomBitsCounter/DIFFICULTY # number of 32 bit words tested
    difficulty = float(num_mined)/numWords # expect this to be P(getting 5 heads in a row in the beginning) = 1/2^5
    print("Experimental difficulty: ",difficulty)
    expected = 1.0/2**5
    print("Expected difficulty: ",expected)
    err = abs(difficulty-expected) / expected * 100
    print("% error: ",err)
if mining:
    print()
else:
    for i in range(10):
        print(str(i)+": "+"".join(ret[i]))
