import RPi.GPIO as GPIO #GPIO module
import paho.mqtt.client as mqtt #mqtt message module
from time import sleep
import os
import time

RECEIVER_PIN = 23
client = mqtt.Client()

# Event handler


def callback_func(channel):
    if GPIO.input(23) == 0:
        client.publish("test/pi", "Lichtschranke aktiv")
    else:
        client.publish("test/pi", "Lichtschranke unterbrochen")


def on_connect(client, userdata, flags, rc):
    client.publish("connected")

# Functions


def init():
    GPIO.setmode(GPIO.BCM)  # gpio direct pcb read mode
    GPIO.setwarnings(False)  # disable gpio warnings
    GPIO.setup(RECEIVER_PIN, GPIO.IN)  # sets mode of specific pin
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH,
                          callback=callback_func, bouncetime=20)  # event listener, bounce time = time to sleep till next event handle
    client.on_connect = on_connect  # publish "connected" on connect
    client.connect("104.45.70.122", 1883, 60)
    client.loop_start()


def run():
    sleep(1)


if __name__ == '__main__':
    init()
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
