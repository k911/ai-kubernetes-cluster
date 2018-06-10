#!/usr/bin/env python3

from main import app

if __name__ == "__main__":
    from main.configuration import host, port, debug

    app.run(host=host, port=port, debug=debug)
