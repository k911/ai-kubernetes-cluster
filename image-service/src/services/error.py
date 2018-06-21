from flask import jsonify


def json_error_resp(message, code):
    status_code = str(code)
    i = len(status_code)
    if i == 4:
        status_code = status_code[:-1]
    elif i != 3:
        raise ValueError("code must be 3 or 4 digits long")

    status_code = int(status_code)
    if status_code < 400 or status_code > 599:
        raise ValueError("resulting status code must be in range 400 to 500")

    return jsonify(dict(message=message, code=code)), status_code
