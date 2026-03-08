from flask import Flask, request
import time
import json

app = Flask(__name__)

latencies = []

@app.route("/sensor", methods=["POST"])
def sensor():

    data = request.json

    timestamp = float(data["timestamp"])

    delay = time.time() - timestamp

    latencies.append(delay)

    metrics = {
        "http_latency": sum(latencies)/len(latencies),
        "http_messages": len(latencies)
    }

    with open("metrics_http.json","w") as f:
        json.dump(metrics,f)

    return {"status":"ok"}

app.run(port=5000)