#!/usr/bin/env python3
# original code
import websocket
import json
from time import sleep
import threading
import numpy as np


################################## MQTT SETUP - optional ##################################
import paho.mqtt.client as mqtt

node_topic="CAS/haptic_feedback"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code", reason_code)

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    # def on_message(client, userdata, msg):
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

BROKER_EDGE_IP =  "10.10.12.24"
BROKER_CLOUD_IP="test.mosquitto.org"
mqtt_send=True  # set to True to enable MQTT sending
if mqtt_send:

    client.connect(BROKER_EDGE_IP, 1883, 60)

    client.loop_start()
    print("connected to mqtt broker EDGE")
#############################################################################################

####################################### XELA Setup ######################################
# custom library imports
import MyXela 
feature_extractor = MyXela.XelaTactileFeatureExtractor()


IP_XELA = "10.2.0.2"

port = 5000  # the port the server is running on
print(f"running client connecting to ws://{IP_XELA}:{port}")
lastmessage = {"message": "No message"}  # default message you will overwrite when you get update

def on_message(wsapp, message):
    global lastmessage  # globalize to overwrite original
    try:
        data = json.loads(message)
    except Exception:
        pass
    else:
        try:
            if data["message"] == "Welcome":  # get the Welcome Message with details, print if you like
                print(data)
            else:
                lastmessage = data
        except Exception:
            pass  # ignore message as it's probably invalid

def threader(target, args=False, **targs):
    # args is tuple of arguments for threaded function other key-value pairs will be sent to Thread
    if args:
        targs["args"] = (args,)
    thr = threading.Thread(target=target, **targs)
    thr.daemon = True
    thr.start()

def mesreader():  # this is your app reading the last valid message you received
    while True:  # to run forever
        try:
            if lastmessage["message"] != "No message":
                
                
                print("extracting feature")
                feature_extractor.extract_force(lastmessage)
                print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
                pub_val=round(np.max(feature_extractor.fz_norm),2)
                print(f"published value (max of Fz norm): {pub_val}")
                payload= json.dumps({"xela_1": pub_val})
                print("publishing topic: ", node_topic, " payload: ", payload)
                if mqtt_send:
                    client.publish(node_topic, payload)  # Publish to topic1
                
            

            t=1.5
            print(f"--- sleeping for {t} seconds ---")
            sleep(t)  # your calculations and processes here (sleep is used as simulation here)
        except KeyboardInterrupt:
            break  # break on KeyboardInterrupt
        except Exception as e:
            print("Exception: {}: {}".format(type(e).__name__, e))

try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(IP_XELA, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
except Exception as e:
    print("Exception: {}: {}".format(type(e).__name__, e))

    exit()