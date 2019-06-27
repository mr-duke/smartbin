import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time
import json

#from mpu6050 import mpu6050
from time import sleep

# DEFINITIONS
#gyro = mpu6050(0x68)

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

client = mqtt.Client()
MQTT_TOPIC = "smartbin"

#GPIO DEFINITIONS

INDICATOR_RED = 17
INDICATOR_GREEN = 27
LIGHTSENSOR_PIN = 23
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#STATES
LID_STATE = ""
FILL_STATE = 0


# Event handler




def on_connect(client, userdata, flags, rc):
    print("connected")



# Functions

def sendSensorData():
    print("anfang")
    print("LID: " + LID_STATE)
    data = {
        "lid":str(LID_STATE),
        "getDistance":getDistance(),
        "timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    client.publish(MQTT_TOPIC, json.dumps(data))
    print(json.dumps(data))

def init(): #sent on GPIO state change
    print("init")
    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings
    #GPIO Pins
    GPIO.setup(INDICATOR_RED, GPIO.OUT) #indicator led
    GPIO.setup(INDICATOR_GREEN, GPIO.OUT) #indicator led
    GPIO.setup(LIGHTSENSOR_PIN
, GPIO.IN)  # sets mode of specific pin
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    #GPIO Output Sets/Resets
    GPIO.output(INDICATOR_RED, GPIO.LOW) # Indicator Reset
    GPIO.output(INDICATOR_GREEN, GPIO.LOW) # Indicator Reset
    #Misc
    GPIO.add_event_detect(LIGHTSENSOR_PIN, GPIO.BOTH, callback=getLidState
, bouncetime=20)  # event listener, bounce time = time to sleep till next event handle
    client.on_connect = on_connect  # publish "connected" on connect
    getLidState("hello")
    print(LID_STATE)
    print("connecting")
    client.connect("infmqtt.westeurope.azurecontainer.io", 1883, 60)
    client.loop_start()

def getDistance():
    GPIO.output(GPIO_TRIGGER, True) # setze Trigger auf HIGH

    # setze Trigger nach 0.01ms auf LOW
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

    TimeElapsed = StopZeit - StartZeit # Zeit Differenz zwischen Start und Ankunft
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    getDistance = (TimeElapsed * 34300) / 2

    Height = 40 #cm
    FILL_PERCENTAGE = (1 - (getDistance / Height))
    if FILL_PERCENTAGE < 0:
        FILL_PERCENTAGE = 0
    print(round((FILL_PERCENTAGE*100)))
    setLedIndicator(round((FILL_PERCENTAGE*100)))
    return getDistance


def setLedIndicator(fillPercentage):
    GPIO.PWM(INDICATOR_RED, fillPercentage + 0.001)
    GPIO.PWM(INDICATOR_GREEN, 100-fillPercentage + 0.001)

def getLidState(param):
    print("got into function, ")
    print("GPIO Light " + str(GPIO.input(23)))
    global LID_STATE
    try:
        if GPIO.input(23) == 0:
            print("offen")
            #offen
            
            LID_STATE = "open"
        else:
            #zu
            print("zu")
            LID_STATE = "closed"
    except Exception as e:
        print(e)



if __name__ == '__main__':
    init()
    i = 0
    try:
        while True: # sends json every x seconds
            getLidState("helloMain")
            sendSensorData()
            sleep(1)
##            for i in range(1,100):
##                sleep(1)
##                if i % 2 == 0:
##                    GPIO.output(INDICATOR_GREEN, 1)
##                else:
##                    GPIO.output(INDICATOR_GREEN, 0)
##                if i % 2 == 1:
##                    GPIO.output(INDICATOR_RED, 1)
##                else:
##                    GPIO.output(INDICATOR_RED, 0)
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
