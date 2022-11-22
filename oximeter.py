# CSCE 462 Lab 1 polling method
# Kevin Yao and Omar Irshad

import RPi.GPIO as GPIO
import time
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

GPIO.setwarnings(False)

	
GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT) #Button


GPIO.output(6,GPIO.HIGH)




spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)

chan0 = AnalogIn(mcp, MCP.P0)

counter = 0
start_time = clock_gettime(0)
while True:
    print(chan0.voltage)
    counter+=1
    if counter>5000:
        break

GPIO.output(6,GPIO.LOW)
    