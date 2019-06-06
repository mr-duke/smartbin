import RPi.GPIO as GPIO
import os, time
import paho.mqtt.client as mqtt
 
RECEIVER_PIN = 23
RECEIVER_PIN2 = 24
 
def callback_func(channel):
        print("Lichtschranke wurde unterbrochen")

def callback_func2(channel):
        print("Lichtschranke wurde geoeffnet")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
 
if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(RECEIVER_PIN, GPIO.IN)
    GPIO.setup(RECEIVER_PIN2, GPIO.IN)
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.RISING, callback=callback_func, bouncetime=200)
    GPIO.add_event_detect(RECEIVER_PIN2, GPIO.FALLING, callback=callback_func2, bouncetime=200)
    
    try:
        while True:
            time.sleep(0.5)
    except:
        # Event wieder entfernen mittels:
        GPIO.remove_event_detect(RECEIVER_PIN)
