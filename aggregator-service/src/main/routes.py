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

    models = parse_models(request.args.getlist("model[]"))
    weights = dict()
    for name, weight in models:
        if name not in USED_SERVICES:
            return json_error_resp(
                'Value "%s" is not an allowed model. Accepted values: %s ' % (name, ', '.join(USED_SERVICES)), 4004)

        try:
            weight = float(weight)
        except ValueError:
            return json_error_resp(
                'Weight "%s" is a valid float.' % str(weight), 4005)

        if weight < 0. or weight > 1.0:
            return json_error_resp(
                'Weight "%s" is not in range (0.0, 1.0).' % str(weight), 4006)

        if name in weights:
            return json_error_resp(
                'Model "%s" is provided more than once.' % name, 4007)

        weights[name] = weight

    return jsonify(aggregate(img, request.args.get("top"), weights)), 200


def parse_models(arg_models: list) -> list:
    if len(arg_models) == 0:
        models = [(name, 1.0) for name in USED_SERVICES]
    else:
        models = []
        for item in arg_models:
            if ',' in item:
                name, weight = item.split(',')
            else:
                name = item
                weight = 1.0
            models.append((name, weight))

    return models
