#!/usr/bin/env python
import time

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("infmqtt.westeurope.azurecontainer.io", 1883, 60)

client.loop_start()

for i in range(100):
    time.sleep(2)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    message =  f"""[
{{
"weight" : {i},
"distance" :98.6,
"gyro_x" :98.6,
"gyro_y" :98.6,
"gyro_z" :98.6,
"timestamp" :"{timestamp}"
}}
]"""
    client.publish("smartbin", message)
