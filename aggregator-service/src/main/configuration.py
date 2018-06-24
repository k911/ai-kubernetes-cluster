import os

app_env = os.environ.get("FLASK_ENV", "production")
host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 5000))

if "1" == os.environ.get("APP_DEBUG", "0"):
    debug = True
else:
    debug = app_env != "production"

service_path = os.environ.get("SERICE_PATH", "image/analyze")
services_urls = {
    "resnet50": os.environ.get("SERVICE_RESNET50_URL", "http://image-service-resnet50"),
    "vgg19": os.environ.get("SERVICE_VGG19_URL", "http://image-service-vgg19"),
    "inceptv3": os.environ.get("SERVICE_INCEPTV3_URL", "http://image-service-inceptv3"),
    "xceptv1": os.environ.get("SERVICE_XCEPTV1_URL", "http://image-service-xceptv1"),
}
