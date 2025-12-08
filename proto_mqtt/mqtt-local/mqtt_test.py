
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