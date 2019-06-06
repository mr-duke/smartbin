import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep

pin = 23
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.publish("connected")

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    client.on_connect = on_connect
    client.connect("104.45.70.122", 1883, 60)
    client.loop_start()

def run():
    if GPIO.input(pin) == GPIO.HIGH:
            client.publish("test/pi", "Unterbrochen")
    else:
        client.publish("test/pi", "Offen")
    sleep(1)

if __name__ == '__main__':
    init()
    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("stopped by user")
    GPIO.cleanup()
