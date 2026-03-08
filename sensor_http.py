import requests
import random
import time
import sys

sensor_id = sys.argv[1]

while True:

    data = {

        "sensor_id":sensor_id,
        "temperature":random.uniform(60,90),
        "vibration":random.uniform(0,10),
        "timestamp":time.time()

    }

    requests.post(
        "http://localhost:5000/sensor",
        json=data
    )

    print("sensor", sensor_id, "sent data")

    time.sleep(1)