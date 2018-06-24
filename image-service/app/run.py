from flask import Flask, jsonify
import datetime


app = Flask(__name__)


@app.route("/")
@app.route("/status")
def status():
    return jsonify(
        date=datetime.datetime.now().isoformat(),
        version=0.1,
    )
