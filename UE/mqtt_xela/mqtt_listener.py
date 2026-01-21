import paho.mqtt.client as mqtt

# Define the MQTT broker and topic
BROKER = "54.89.231.201"  # Replace with your broker address
PORT = 1883  # Default MQTT port
TOPIC_LIST = ["CAS/haptic_feedback", "UE/to_toy_arm"]  # Replace with your topic

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
        for topic in TOPIC_LIST:
            client.subscribe(topic)
        print(f"Subscribed to topics: {', '.join(TOPIC_LIST)}")
    else:
        print(f"Failed to connect, return code {reason_code}")

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message from topic '{msg.topic}': {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER, PORT, 60)

# Start the MQTT client loop to listen for messages
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting from MQTT Broker...")
    client.disconnect()

