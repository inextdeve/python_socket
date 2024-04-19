import paho.mqtt.client as mqtt

# Define the MQTT parameters
mqtt_host = "mqtt"
mqtt_port = 1883
mqtt_username = "whole_shrimp"
mqtt_password = "LgYOkZak"
mqtt_topic = "yinkana/whole_shrimp/+"

# Define callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(mqtt_topic)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

# Create MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Set username and password
client.username_pw_set(mqtt_username, mqtt_password)

# Connect to MQTT broker
client.connect(mqtt_host, mqtt_port, keepalive=60)

# Start the MQTT loop
client.loop_forever()
