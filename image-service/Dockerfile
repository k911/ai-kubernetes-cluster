FROM python:3.6-alpine3.7
RUN pip install pipenv

COPY docker-app-run.sh /usr/local/bin/docker-app-run
RUN chmod +x /usr/local/bin/docker-app-run

ENV FLASK_APP=app/run.py \
    FLASK_ENV=production \
    HOST=0.0.0.0 \
    PORT=80

WORKDIR /usr/src/app
CMD ["docker-app-run"]

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . /usr/src/api

