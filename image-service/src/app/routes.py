from flask import jsonify

from app import app
from services import status


@app.route("/")
@app.route("/status")
def status_route():
    return jsonify(status.get()), 200
