import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time
import json

from mpu6050 import mpu6050
from time import sleep

gyro = mpu6050(0x68)

# GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
RECEIVER_PIN = 23
client = mqtt.Client()

# Event handler


def callback_func(channel):
    if GPIO.input(23) == 0:
        client.publish("smartbin", "Lichtschranke aktiv")
    else:
        client.publish("smartbin", "Lichtschranke unterbrochen")


def on_connect(client, userdata, flags, rc):
    client.publish("connected")

# Functions


def sendSensorData(): 
    data = {
        "gyro_x":gyro.get_accel_data()['x'], 
        "gyro_y":gyro.get_accel_data()['y'],
        "gyro_z":gyro.get_accel_data()['z'],
        "distance":distance()
    }
    client.publish("smartbin", json.dumps(data))

def init(): #sent on GPIO state change
    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings
    GPIO.setup(RECEIVER_PIN, GPIO.IN)  # sets mode of specific pin
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH,
                          callback=callback_func, bouncetime=20)  # event listener, bounce time = time to sleep till next event handle
    client.on_connect = on_connect  # publish "connected" on connect
    client.connect("104.45.70.122", 1883, 60)
    client.loop_start()

def distance():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distance = (TimeElapsed * 34300) / 2

    return distance






if __name__ == '__main__':
    init()
    try:
        while True: # sends json every x seconds
            sendSensorData()
            sleep(1)
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
