#!/usr/bin/env python
import paho.mqtt.client as mqtt
import requests
import json

server = "infmqtt.westeurope.azurecontainer.io"
powerBiURL = "https://api.powerbi.com/beta/15f1a6d8-cd31-4fbe-81fb-21240240147d/datasets/b6a0d838-0a65-4458-a83b-4fd8f2f65ea7/rows?key=fyK6Ak%2F5svz2LS8UZ9fvUPA0tz%2BWZEjy%2F61zJBNaorslAtGors20FQxV4zXHEeOQZCfoP9LJNl4FJg39C0bVbg%3D%3D"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("smartbin")

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    try:
        data = json.loads(msg.payload)
    except Exception as e:
        print(e)
    print(data)
    #for key, value in data.items():
    #    print (key, value)
    try:
        r = requests.post(powerBiURL, json=data)
        if r == None:
            print("no response")
        else:
            print(r.status_code)
    except Exception as e:
        print(e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, 1883, 60)

client.loop_forever()
