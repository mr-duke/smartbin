import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

hx = HX711(5, 6)


def cleanAndExit():
    GPIO.cleanup()
    sys.exit()


def setup():
    hx.set_offset(7967722.875)
    hx.set_scale(-1.33)


def loop():
    try:
        val = hx.get_grams()
        print(val)
        hx.power_down()
        time.sleep(.001)
        hx.power_up()
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


##################################

if __name__ == "__main__":
    setup()
    while True:
        loop()
