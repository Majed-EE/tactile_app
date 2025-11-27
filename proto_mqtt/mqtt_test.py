#hi
# import paho.mqtt.client as mqtt
# import time

# # Callback when connecting to the broker
# def on_connect(client, userdata, flags, reason_code, properties):
#     print(f"Connected with result code {reason_code}")
#     # Subscribe to a topic
#     client.subscribe("test/topic")

# # Callback when receiving a message
# def on_message(client, userdata, msg):
#     print(f"Received message on {msg.topic}: {msg.payload.decode()}")

# ip_list=["test.mosquitto.org"]
# ip_indx=0
# broker=ip_list[ip_indx]


# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # create new instance
# print("connecting to broker", broker)
# client.connect(broker, 1883, 60) # connect to the broker
# time.sleep(4)
# print("disconnecting")
# client.disconnect() # disconnect

import paho.mqtt.client as mqtt
import time
import ssl


def on_connect(client,userdata, flags,rc):
    if rc==0:
        print("connect OK")
    else:
        print("bad connection returned code= ",rc)

def on_log(client,userdata,level,buf):
    print("log: "+buf)



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Disable certificate verification
# bind call back function
client.on_connect=on_connect
client.on_log=on_log
print("starting")
try:
    
    client.connect("test.mosquitto.org", 8883, 60)

    print("Connected successfully on port 8883!")
    
    # Publish test message
    topic="test/topiczzz"
    msg="Hello Cloud MQTT!"
    client.publish("test/topiczzz", "Hello Cloud MQTT!")

    client.loop_start()
    # we need the loop for callback to process
    time.sleep(4)

    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"Failed to connect: {e}")