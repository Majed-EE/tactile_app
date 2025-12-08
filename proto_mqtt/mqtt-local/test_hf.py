import paho.mqtt.client as mqtt
import numpy as np
import json
import time as T
# ====== CONFIGURE THESE ======
BROKER_ADDRESS = "10.10.7.199"    # Same broker IP
BROKER_PORT = 1883
MQTT_TOPIC_PUB = "CAS/haptic_feedback"
# =============================



def simple_subscriber():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Subscriber connected!")
            client.subscribe("UE/to_toy_arm")
            client.subscribe("CAS/haptic_feedback")
        else:
            print(f"Connection failed: {reason_code}")
    
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            print(f"Received from topic {msg.topic}: {data}")
        except:
            print(f"Received raw: {msg.payload.decode()}")
    
    client.on_connect = on_connect
    client.on_message = on_message
    local_broker=True
    broker_local_address="10.10.7.199"
    broker_address = broker_local_address if local_broker else "test.mosquitto.org"
    print(f"connected to {broker_address}")
    client.connect(broker_address, 1883, 60)
    client.loop_start()
    try:
        while True:
                # This will block and keep listening for messages
            print("Listening for messages...")
            HF_list = list(np.round(np.random.uniform(0, 0.98, 5), 3))
            payload=json.dumps(HF_list)
            client.publish(MQTT_TOPIC_PUB, payload)
            print(f"haptic feedback {HF_list}")
            T.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("MQTT connection closed.")

    # This will block and keep listening for messages
        # print("Listening for messages...")
        # HF_list = list(np.round(np.random.uniform(0, 0.98, 5), 3))
        # payload=json.dumps(HF_list)
        # client.publish(MQTT_TOPIC_PUB, payload)
        # print(f"haptic feedback {HF_list}")
        # T.sleep(0.5)









if __name__ == "__main__":
    simple_subscriber()