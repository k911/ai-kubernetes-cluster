FROM python:3.6-slim
RUN apt-get update && apt-get -y install build-essential

COPY docker-app-run.sh /usr/local/bin/docker-app-run
RUN chmod +x /usr/local/bin/docker-app-run

ENV FLASK_ENV=production \
    APP_DEBUG=0 \
    HOST=0.0.0.0 \
    PORT=80 \
    PYTHONPATH="$PYTHONPATH:/usr/src/app/src"

WORKDIR /usr/src/app
CMD ["docker-app-run"]

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/models/__init__.py /usr/src/app/src/models/__init__.py

ARG APP_MODEL=vgg19
ENV APP_MODEL=$APP_MODEL

# Fetch Keras model data
RUN python3 -c "from models import get_model; get_model('$APP_MODEL')"

# Fetch ImageNet class index
RUN python3 -c "from keras.applications.imagenet_utils import CLASS_INDEX_PATH, get_file; get_file('imagenet_class_index.json', CLASS_INDEX_PATH, cache_subdir='models', file_hash='c2c37ea517e94d9795004a39431a14cb')"

COPY . /usr/src/app
