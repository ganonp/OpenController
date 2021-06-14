#!/usr/bin/env python3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from serial import Serial
import time

import json

ser17 = Serial('/dev/ttyACM0', 9600, timeout=1)
ser2 = Serial('/dev/ttyACM1', 9600, timeout=1)
ser3 = Serial('/dev/ttyACM2', 9600, timeout=1)

interrupt17 = 17
GPIO.setup(interrupt17, GPIO.OUT)

interrupt2 = 2
GPIO.setup(interrupt2, GPIO.OUT)

ser17.flush()
ser2.flush()
while True:
    for interrupt, ser in [(interrupt2, ser2), (interrupt17, ser17)]:
        for x in [0, 1, 2]:
            GPIO.output(interrupt, GPIO.HIGH)
            command = 'data' + str(x) + "\n"
            ser.write(bytes(command.encode('utf-8')))
            pico_data = ser.readline()
            pico_data1 = pico_data.decode("utf-8", "ignore")
            sensor_response = pico_data1[:-2]
            print(sensor_response)
            GPIO.output(interrupt, GPIO.LOW)
    time.sleep(10)
    ser17.flush()
    ser2.flush()

data = json.loads(sensor_response)
print("Index: " + str(data["index"]))
print("Average Output: " + str(data["averaged"]))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from serial import Serial
import time

import json

ser17 = Serial('/dev/ttyACM0', 9600, timeout=1)
ser2 = Serial('/dev/ttyACM1', 9600, timeout=1)
ser3 = Serial('/dev/ttyACM2', 9600, timeout=1)

interrupt17 = 17
GPIO.setup(interrupt17, GPIO.OUT)

interrupt2 = 2
GPIO.setup(interrupt2, GPIO.OUT)

ser17.flush()
ser2.flush()
GPIO.output(interrupt2, GPIO.HIGH)
command = 'init' + "\n"
ser2.write(bytes(command.encode('utf-8')))
pico_data = ser2.readline()
pico_data1 = pico_data.decode("utf-8", "ignore")
sensor_response = pico_data1[:-2]
print(sensor_response)
GPIO.output(interrupt2, GPIO.LOW)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from serial import Serial
import time

ser3 = Serial('/dev/ttyACM2', 9600, timeout=1)
interrupt3 = 3
GPIO.setup(interrupt3, GPIO.OUT)
GPIO.output(interrupt3, GPIO.HIGH)
command = "0on" + "\n"
ser3.write(command.encode('utf-8'))
pico_data = ser3.readline()
pico_data1 = pico_data.decode("utf-8", "ignore")
sensor_response = pico_data1[:-2]
print(sensor_response)
GPIO.output(interrupt3, GPIO.LOW)
time.sleep(1)
GPIO.output(interrupt3, GPIO.HIGH)
command = "0off " + "\n"
ser3.write(command.encode('utf-8'))
pico_data = ser3.readline()
pico_data1 = pico_data.decode("utf-8", "ignore")
sensor_response = pico_data1[:-2]
print(sensor_response)
GPIO.output(interrupt3, GPIO.LOW)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from serial import Serial
import time

ser3 = Serial('/dev/ttyACM0', 9600, timeout=1)

interrupt3 = 3

GPIO.setup(interrupt3, GPIO.OUT)
GPIO.output(interrupt3, GPIO.HIGH)

command = "stat1off" + "\n"
# command = "init"
ser3.write(command.encode('utf-8'))
pico_data = ser3.readline()
pico_data1 = pico_data
sensor_response = pico_data1[:-2]
print(sensor_response)

GPIO.output(interrupt3, GPIO.LOW)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from serial import Serial
import time

ser3 = Serial('/dev/ttyACM1', 9600, timeout=1)

interrupt3 = 17

GPIO.setup(interrupt3, GPIO.OUT)
GPIO.output(interrupt3, GPIO.HIGH)

command = 'init'+'\n'
ser3.write(command.encode('utf-8'))
pico_data = ser3.readline()
pico_data1 = pico_data
sensor_response = pico_data1[:-2]
print(sensor_response)

GPIO.output(interrupt3, GPIO.LOW)
