from flask import Flask, jsonify, send_file
import json

app = Flask(__name__)

@app.route("/")
def dashboard():
    return send_file("templates/index.html")

@app.route("/metrics")
def metrics():

    try:
        with open("metrics_http.json") as f:
            http = json.load(f)
    except:
        http = {}

    try:
        with open("metrics.json") as f:
            mqtt = json.load(f)
    except:
        mqtt = {}

    return jsonify({
        "http": http,
        "mqtt": mqtt
    })

app.run(port=8000)