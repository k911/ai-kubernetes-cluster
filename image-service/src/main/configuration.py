import os

app_env = os.environ.get("FLASK_ENV", "production")
app_model = os.environ.get("APP_MODEL", "resnet50")
host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 5000))

if "1" == os.environ.get("APP_DEBUG", "0"):
    debug = True
else:
    debug = app_env != "production"

if app_model != "inceptv3" and app_model != "xceptv1":
    img_target = (224, 224)
else:
    img_target = (299, 299)
