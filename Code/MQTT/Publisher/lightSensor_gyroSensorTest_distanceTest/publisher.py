import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time
import json

from mpu6050 import mpu6050
from time import sleep

gyro = mpu6050(0x68)

##while True:
##    accel_data = gyro.get_accel_data()
##    gyro_data = gyro.get_gyro_data()
##    temp = gyro.get_temp()
##
##    print("Accelerometer data")
##    print("x: " + str(accel_data['x']))
##    print("y: " + str(accel_data['y']))
##    print("z: " + str(accel_data['z']))
##
##    print("Gyroscope data")
##    print("x: " + str(gyro_data['x']))
##    print("y: " + str(gyro_data['y']))
##    print("z: " + str(gyro_data['z']))
##
##    print("Temp: " + str(temp) + " C")
##    sleep(0.5)



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
        "gyro_z":gyro.get_accel_data()['z']
    }
    client.publish(json.dumps(x))

def init(): #sent on GPIO state change
    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings
    GPIO.setup(RECEIVER_PIN, GPIO.IN)  # sets mode of specific pin
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH,
                          callback=callback_func, bouncetime=20)  # event listener, bounce time = time to sleep till next event handle
    client.on_connect = on_connect  # publish "connected" on connect
    client.connect("104.45.70.122", 1883, 60)
    client.loop_start()


if __name__ == '__main__':
    init()
    try:
        while True: # sends json every x seconds
            
            sleep(1)
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
