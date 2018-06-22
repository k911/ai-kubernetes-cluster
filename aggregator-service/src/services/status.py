import datetime
import socket

from main.configuration import debug, app_env, host, port, services_urls, service_path


def get():
    data = {
        "version": 0.2,
        "date": datetime.datetime.now().isoformat()
    }

    if debug:
        data["network"] = {
            "host": socket.gethostname(),
            "ip": socket.gethostbyname(socket.gethostname())
        }
        data["configuration"] = {
            "debug": debug,
            "env": app_env,
            "host": host,
            "port": port,
            "service": {
                "path": service_path,
                "urls": services_urls
            }
        }

    return data
