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
    client.connect("test.mosquitto.org", 1883, 60)
    
    # This will block and keep listening for messages
    print("Listening for messages...")
    for x in range(100):
        print(f"Waiting... {x+1}/100")
        client.loop_start()
        time.sleep(1)
    client.loop_stop()

if __name__ == "__main__":
    simple_subscriber()
    print("Subscriber finished.")