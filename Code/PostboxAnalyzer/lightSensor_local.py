import RPi.GPIO as GPIO
import os, time
 
RECEIVER_PIN = 23

def callback_func(channel):
        if GPIO.input(23) == 0:
                print("Lichtschranke aktiv")
        else:
                print("Lichtschranke unterbrochen")


 
if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(RECEIVER_PIN, GPIO.IN)
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=callback_func, bouncetime=500)
    
    try:
        while True:
            time.sleep(0.5)
    except:
        # Event wieder entfernen mittels:
        GPIO.remove_event_detect(RECEIVER_PIN)
