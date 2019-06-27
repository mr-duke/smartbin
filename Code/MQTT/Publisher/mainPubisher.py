import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time
import json
from hx711 import HX711

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

PUBLISHING_INTERVAL = 1

#GPIO DEFINITIONS

INDICATOR_RED = 17
INDICATOR_GREEN = 27
LIGHTSENSOR_PIN = 23
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#STATES
LID_STATE = ""
FILL_PERCENTAGE = 0

#weight
hx = HX711(5, 6)
WEIGHT = 0

def on_connect(client, userdata, flags, rc):
    print("connected")

# Functions

def sendSensorData():
    print("anfang")
    print("LID: " + LID_STATE)
    data = {
        "Lid":LID_STATE,
        "Distance":getDistance(),
        "FillPercentage":FILL_PERCENTAGE,
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
    
    #GPIO Output Sets/Resets
    #GPIO.output(INDICATOR_RED, GPIO.LOW) # Indicator Reset
    #GPIO.output(INDICATOR_GREEN, GPIO.LOW) # Indicator Reset
    #Misc
    #GPIO.add_event_detect(LIGHTSENSOR_PIN, GPIO.BOTH, callback=getLidState, bouncetime=20)  # event listener, bounce time = time to sleep till next event handle
    client.on_connect = on_connect  # publish "connected" on connect
    getLidState("hello")
    print(LID_STATE)

    hx.set_offset(7967722.875)
    hx.set_scale(-1.33)
    
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

    Height = 40 #cm
    global FILL_PERCENTAGE
    FILL_PERCENTAGE = int(round((1 - (getDistance / Height))*100))
    if FILL_PERCENTAGE < 0:
        FILL_PERCENTAGE = 0
    if FILL_PERCENTAGE >= 90:
        FILL_PERCENTAGE = 99
    elif FILL_PERCENTAGE >= 50:
        FILL_PERCENTAGE += 10
    print(FILL_PERCENTAGE)
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
    print("fill percentage in setLEDFunction ---  " + str(fillPercentage))
    red.ChangeDutyCycle(fillPercentage + 0.0001)
    green.ChangeDutyCycle(100-fillPercentage)

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

    try:
        while True: # sends json every x seconds
            getLidState("helloMain")
            sendSensorData()
            sleep(PUBLISHING_INTERVAL)

    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
