import paho.mqtt.client as mqtt

# ====== CONFIGURE THESE ======
BROKER_ADDRESS = "10.10.7.199"    # Same broker IP
BROKER_PORT = 1883
MQTT_TOPIC_PUB = "servo/angle"
# =============================

print("hi")
def main():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    client.loop_start()  # optional background loop (for reliability)

    print("MQTT Servo Angle Sender")
    print("Type angle (0–180) or 'q' to quit.\n")

    try:
        while True:
            user_input = input("Angle: ").strip()
            if user_input.lower() == 'q':
                break

            # Simple check
            try:
                angle = int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if angle < 0 or angle > 180:
                print("Angle must be between 0 and 180.")
                continue

            payload = str(angle)
            client.publish(MQTT_TOPIC_PUB, payload)
            print(f"[MQTT] Published {payload} to {MQTT_TOPIC_PUB}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("MQTT connection closed.")


if __name__ == "__main__":
    main()