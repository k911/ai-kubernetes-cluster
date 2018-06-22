from flask import jsonify, request

from main import app
from services import status
from services.aggregator import aggregate, USED_SERVICES
from services.error import json_error_resp
from services.image import allowed_extension, ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/status")
def status_route():
    return jsonify(status.get()), 200


@app.route("/image/aggregate", methods=['POST'])
def image_analyze_route():
    if "image" not in request.files:
        return json_error_resp('No "image" file in request body.', 4001)
    img = request.files['image']
    if img.filename == '':
        return json_error_resp("No selected image file.", 4002)

    if not allowed_extension(img.filename):
        return json_error_resp(
            'Extension of provided file is not within allowed ones: "%s"' % (', '.join(ALLOWED_EXTENSIONS)), 4003)

    models = request.args.get("models")

    if models is not None:
        models = models.split(',')
        for model in models:
            if model not in USED_SERVICES:
                return json_error_resp(
                    'Value "%s" is not an allowed model. Accepted values: %s ' % (model, ', '.join(USED_SERVICES)), 4004)
    else:
        models = USED_SERVICES

    return jsonify(aggregate(img, request.args.get("top"), models)), 200
