import paho.mqtt.client as mqtt  # mqtt message module
import RPi.GPIO as GPIO  # GPIO module
import os
from time import sleep
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

hx = HX711(5, 6)
weight_diff_tolerance = 0.2
weight_multiplier = 2


def cleanAndExit():
    GPIO.cleanup()
    sys.exit()


def setup():
    hx.set_offset(7995659.1875)
    hx.set_scale(-26.866)


def loop():
    try:
        val = hx.get_grams()
        hx.power_down()
        # mqtt part start
        #
        if abs(val-last_val) < weight_diff_tolerance:
            client.publish("test/pi", val * weight_multiplier)
            time.sleep(1)
            hx.power_up()
            last_val = val
        #
        # mqtt part end
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


# weight sensor only

if __name__ == "__main__":
    setup()
    while True:
        loop()


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
    setup()
    while True:
        loop()
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
