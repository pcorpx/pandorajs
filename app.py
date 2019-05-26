import requests
from flask import Flask, render_template, request, jsonify, json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("my.html")

@app.route("/pandora/<string:test>")
def get(test):
    selectdata = {"choices" : []}
    dlist = []
    with open("data.json", 'r', encoding="utf8") as f:
        data = json.loads(f.read())
    for item in data['choices']:
        if item['label'].lower().startswith(test.lower()):
            dlist.append(item)
    selectdata["choices"] = dlist
    return jsonify(selectdata)
