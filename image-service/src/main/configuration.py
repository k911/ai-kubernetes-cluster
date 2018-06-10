import os

app_env = os.environ.get("FLASK_ENV", "production")
host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 5000))

if "1" == os.environ.get("APP_DEBUG", "0"):
    debug = True
else:
    debug = app_env != "production"
