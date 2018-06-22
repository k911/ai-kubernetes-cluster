import io

from flask import jsonify, request
from main import app
from main.configuration import img_target, app_model
from services import status, image
from PIL import Image
from services.error import json_error_resp
from services.image import allowed_extension, ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/status")
def status_route():
    return jsonify(status.get()), 200


@app.route("/image/analyze", methods=['POST'])
def image_analyze_route():
    if "image" not in request.files:
        return json_error_resp('No "image" file in request body.', 4001)
    img = request.files['image']
    if img.filename == '':
        return json_error_resp("No selected image file.", 4002)

    if not allowed_extension(img.filename):
        return json_error_resp(
            'Extension of provided file is not within allowed ones: "%s"' % (', '.join(ALLOWED_EXTENSIONS)), 4003)

    img = img.read()
    img = Image.open(io.BytesIO(img))

    return jsonify(image.analyze(img, img_target, app_model, request.args.get("top"))), 200
