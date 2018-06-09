import os

app_env = os.environ.get("FLASK_ENV", "production")
debug = app_env != "production"
host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 5000))
