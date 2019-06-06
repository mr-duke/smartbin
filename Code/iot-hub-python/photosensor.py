import RPi.GPIO as GPIO
import os, time

PIN = 23

class Photosensor(object):
    def __init__(self, **kwargs):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(PIN, GPIO.IN)

    def readSensor():
        if GPIO.input(PIN, GPIO.HIGH):
            return "HIGH"
        else return "LOW"
