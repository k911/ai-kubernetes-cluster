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

COPY . /usr/src/app
