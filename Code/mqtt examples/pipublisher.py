import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep

rot = 18
gruen = 15
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    GPIO.output(gruen, GPIO.HIGH)
    sleep(1)
    GPIO.output(gruen, GPIO.LOW)

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rot, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(gruen, GPIO.OUT, initial=GPIO.LOW)
    client.on_connect = on_connect
    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_start()

def run():
    message = input()
    client.publish("test/pi", message)
    GPIO.output(gruen, GPIO.HIGH)
    sleep(0.25)
    GPIO.output(gruen, GPIO.LOW)

if __name__ == '__main__':
    init()
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
