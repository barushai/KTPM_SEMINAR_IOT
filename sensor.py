import paho.mqtt.client as mqtt
import random
import time
import sys

sensor_id = sys.argv[1]

broker = "broker.hivemq.com"
topic = "iot/demo/engine"

client = mqtt.Client()
client.connect(broker,1883)

while True:

    temperature = random.uniform(60,90)
    vibration = random.uniform(0,10)

    payload = f"{sensor_id},{temperature},{vibration},{time.time()}"

    client.publish(topic, payload)

    print(f"sensor {sensor_id} send:", payload)

    time.sleep(1)