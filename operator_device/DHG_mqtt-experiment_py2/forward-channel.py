from flask import Flask, request, render_template, jsonify
import time
import numpy as np
from bidirectional_control_DHG import DHG_Bidirectional
import paho.mqtt.client as mqtt
import json
import logging
logging.basicConfig(filename='pinch.log', level=logging.INFO, format='%(asctime)s %(message)s')


N=10

def call_stiff_changer():
    pass


###########################################3 MQTT Block #####################################
# MQTT Settings
BROKER = "10.10.7.199"     # Change to IP if remote
PORT = 1883
TOPIC_PUB = "UE/to_toy_arm"
TOPIC_SUB = "CAS/haptic_feedback" # tactile feedback stream
mqtt_connect=False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to broker")
        client.subscribe(TOPIC_SUB)
        print(" Subscribed to: " + TOPIC_SUB)
    else:
        print(" Connection failed")

# When message received
def on_message(client, userdata, msg):
    print("Message received")
    data=json.loads(msg.payload.decode())
    print("Topic:", msg.topic)
    print("Message:", data)
    if msg.topic==TOPIC_SUB:
        print("updating stiffness {}".format(data[0]))
        logging.info("updating stiffness {}".format(data[0]))
        call_stiff_changer(data[0])
        
    #test_write_worker


# Create client
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message



# Connect to broker
if mqtt_connect:
    client.connect(BROKER, PORT, 60)
    client.loop_start()


####################################### MQTT end #########################################




##################################### DHG Controler block ####################################

import time as T

print("Iteration 1-> ")

dhg_device=DHG_Bidirectional()
dhg_device.connect()

print("Device connected: ", dhg_device.is_dhg_connected)
logging.info("Device connected: ", dhg_device.is_dhg_connected)
# once device connected, for Feedback direction, set stiffness and set point

############################################################################



###################################### Forward control -> Frame Read #####################################3

dhg_device.set_frame_read_worker()

dhg_device.publish_joint_state()

print("starting in 5 seconds")

time.sleep(5)
########################################################################################



######################################################## main loop ###############################

for itr in range(N):
    dhg_device.publish_joint_state() # have to do it everytime else it will feeze
    valset=dhg_device.Joint.position
    print("inside loop demo")
    print("thumb: {0}".format(valset[2])) # thumb
    print("index: {0}".format(valset[4])) # index
    print("middle: {0}".format(valset[6])) # middle   
    print("ring: {0}".format(valset[8])) # ring
    print("pinky: {0}".format(valset[10])) # pinky
    t=1
    print("sleeping for {} seconds".format(t))
    print("hf received: ")
    
    if mqtt_connect:
        data_finger=[valset[4],valset[6]]
        print("publsing: {}".format(data_finger))  # publish forward channel control
        payload=json.dumps(data_finger) #.tobytes()

    
        client.publish(TOPIC_PUB, payload)
    
    T.sleep(0.5)

if mqtt_connect:
    client.loop_stop()
    print("closing mqtt connection")

print("resting")
dhg_device.set_rest()
print("ending")
