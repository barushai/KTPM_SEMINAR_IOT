import paho.mqtt.client as mqtt
import time
import json

broker = "broker.hivemq.com"
topic = "iot/demo/engine"

latencies = []
messages = 0

def on_message(client, userdata, msg):

    global messages

    payload = msg.payload.decode()

    sensor_id,temp,vib,timestamp = payload.split(",")

    delay = time.time() - float(timestamp)

    latencies.append(delay)

    messages += 1

    metrics = {
        "mqtt_latency": sum(latencies)/len(latencies),
        "mqtt_messages": messages
    }

    with open("metrics.json","w") as f:
        json.dump(metrics,f)

    print("MQTT message", messages)

client = mqtt.Client()

client.connect(broker,1883)

client.subscribe(topic)

client.on_message = on_message

client.loop_forever()