import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time
import json
from hx711 import HX711
from time import sleep

# DEFINITIONS

client = mqtt.Client()
MQTT_TOPIC = "smartbin"

PUBLISHING_INTERVAL = 0.5

#GPIO DEFINITIONS

INDICATOR_RED = 17
INDICATOR_GREEN = 27
LIGHTSENSOR_PIN = 23
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#STATES
LID_STATE = ""
LID_BOOL = 0
FILL_PERCENTAGE = 0

#weight
hx = HX711(5, 6)
WEIGHT = 0

def on_connect(client, userdata, flags, rc):
    print("connected")

# Functions

def sendSensorData():
    data = {
        "Lid":LID_STATE,
        "LidBool":LID_BOOL,
        "Distance":getDistance(),
        "FillPercentage":FILL_PERCENTAGE,
        "MaxPercentage":100,
        "Weight":getWeight(),
        "Timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    if LID_STATE == "open":
       data["Distance"] = -1
       data["FillPercentage"] = -1
    client.publish(MQTT_TOPIC, json.dumps(data))
    print(json.dumps(data))

def init(): #sent on GPIO state change
    print("init")

    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings

    #GPIO Pins
    GPIO.setup(INDICATOR_RED, GPIO.OUT) #indicator led
    GPIO.setup(INDICATOR_GREEN, GPIO.OUT) #indicator led
    GPIO.setup(LIGHTSENSOR_PIN, GPIO.IN)  # sets mode of specific pin
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    #indicator
    global red
    red = GPIO.PWM(INDICATOR_RED, 100)
    global green
    green = GPIO.PWM(INDICATOR_GREEN, 100)

    red.start(100)
    green.start(100)
    
    client.on_connect = on_connect  # publish "connected" on connect
    getLidState("hello")

    hx.set_offset(7967413.5)
    hx.set_scale(-1.3103896103896104)
    
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
    getDistance = int(round((TimeElapsed * 34300) / 2))

    Height = 35 #cm
    global FILL_PERCENTAGE
    distance = getDistance
    if distance > 35 and distance < 45:
        distance = 35
    FILL_PERCENTAGE = int(round((1 - (distance / Height))*100))
    if LID_BOOL == 1:
        FILL_PERCENTAGE = -1
##    if FILL_PERCENTAGE >= 90:
##        FILL_PERCENTAGE = 99
##    elif FILL_PERCENTAGE >= 50:
##        FILL_PERCENTAGE += 10
    setLedIndicator(FILL_PERCENTAGE)
    return getDistance

def getWeight():
    global WEIGHT
    WEIGHT = int(round(hx.get_grams()))
    hx.power_down()
    time.sleep(.001)
    hx.power_up()
    return WEIGHT

def setLedIndicator(fillPercentage):
    dutycycle = fillPercentage
    if dutycycle < 0:
        dutycycle = 100
    if dutycycle > 100:
        dutycycle = 100
    red.ChangeDutyCycle(dutycycle)
    green.ChangeDutyCycle(100-dutycycle)

def getLidState(param):
    global LID_STATE
    global LID_BOOL
    try:
        if GPIO.input(23) == 0:
            #offen
            LID_STATE = "open"
            LID_BOOL = 1
        else:
            #zu
            LID_STATE = "closed"
            LID_BOOL = 0
    except Exception as e:
        print(e)



if __name__ == '__main__':
    init()

    try:
        while True: # sends json every x seconds
            getLidState("helloMain")
            sendSensorData()
            sleep(PUBLISHING_INTERVAL)

    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
