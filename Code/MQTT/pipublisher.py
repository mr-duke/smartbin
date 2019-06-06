import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep
import RPi.GPIO as GPIO
import os
import time

RECEIVER_PIN = 23
client = mqtt.Client()

# Main function


if __name__ == '__main__':
    init()
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()

# Event handler


def callback_func(channel):
    if GPIO.input(23) == 0:
        print("Lichtschranke aktiv")
    else:
        print("Lichtschranke unterbrochen")


def on_connect(client, userdata, flags, rc):
    client.publish("connected")

# Functions


def init():
    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings
    GPIO.setup(RECEIVER_PIN, GPIO.IN)  # sets mode of specific pin
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH,
                          callback=callback_func, bouncetime=500)  # event listener
    client.on_connect = on_connect  # publish "connected" on connect
    client.connect("104.45.70.122", 1883, 60)
    client.loop_start()


def run():
    sleep(1)