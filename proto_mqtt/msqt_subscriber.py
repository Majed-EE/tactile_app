import paho.mqtt.client as mqtt
import time
import json



def simple_subscriber():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Subscriber connected!")
            client.subscribe("test/topic2")
        else:
            print(f"Connection failed: {reason_code}")
    
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            print(f"Received: {data}")
        except:
            print(f"Received raw: {msg.payload.decode()}")
    
    client.on_connect = on_connect
    client.on_message = on_message
    local_broker=True
    broker_local_address="10.10.7.199"
    broker_address = broker_local_address if local_broker else "test.mosquitto.org"
    client.connect(broker_address, 1883, 60)
    
    # This will block and keep listening for messages
    print("Listening for messages...")
    t_run=30
    for x in range(t_run):
        print(f"Waiting... {x+1}/{t_run}")
        client.loop_start()
        time.sleep(1)
    client.loop_stop()

if __name__ == "__main__":
    simple_subscriber()
    print("Subscriber finished.")