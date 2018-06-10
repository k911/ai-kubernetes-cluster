import datetime
import socket

from main.configuration import debug, app_env, host, port


def get():
    data = {
        "version": 0.1,
        "date": datetime.datetime.now().isoformat()
    }

    if debug:
        data["docker"] = {
            "host": socket.gethostname(),
            "ip": socket.gethostbyname(socket.gethostname())
        }
        data["configuration"] = {
            "debug": debug,
            "app_env": app_env,
            "host": host,
            "port": port
        }

    return data
