#!/usr/bin/env python3

from app import app

if __name__ == "__main__":
    from app.configuration import app_env, host, port

    app.run(host=host, port=port, debug=(True, None)[app_env == "production"])
