import datetime
import socket

from main.configuration import debug, app_env, host, port, app_model, img_target
from services.image import dimensions


def get():
    data = {
        "version": 0.2,
        "date": datetime.datetime.now().isoformat(),
    }

    if debug:
        data["network"] = {
            "host": socket.gethostname(),
            "ip": socket.gethostbyname(socket.gethostname())
        }
        data["configuration"] = {
            "debug": debug,
            "env": app_env,
            "model": dict(name=app_model, target=dimensions(img_target)),
            "host": host,
            "port": port
        }
    else:
        data["model"] = app_model

    return data
