FROM python:3.6-alpine3.7
RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev && \
    pip install pipenv

COPY docker-app-run.sh /usr/local/bin/docker-app-run
RUN chmod +x /usr/local/bin/docker-app-run

ENV FLASK_ENV=production \
    APP_DEBUG=0 \
    HOST=0.0.0.0 \
    PORT=80 \
    PYTHONPATH="$PYTHONPATH:/usr/src/app/src"

WORKDIR /usr/src/app
CMD ["docker-app-run"]

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . /usr/src/app

