import paho.mqtt.client as mqtt
import blob
import json
import uuid

SERVER = "infmqtt.westeurope.azurecontainer.io"
TOPIC = "smartbin"

blob = blob.Blob(TOPIC)


def send_to_blob(data):
    print("Send to blob: " + data)
    blob.write_data_to_blob(data)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    b = str(msg.payload.decode("utf-8"))
    print(msg.topic + " " + b)
    send_to_blob(b)


# Main
if __name__ == '__main__':
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(SERVER, 1883, 60)

        client.loop_forever()
    
    except Exception as e:
        print("Error occured: {0}".format(e.args))