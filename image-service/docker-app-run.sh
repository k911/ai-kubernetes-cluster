#!/bin/bash

if [[ "$FLASK_ENV" = 'development' ]] || [[ "$APP_DEBUG" = '1' ]]; then
    python3 src/run.py # flask development server (with hot reloading)
else
    uwsgi --http $HOST:$PORT --wsgi-file src/uwsgi.py
fi;
