FROM python:3.6-alpine3.7
RUN pip install pipenv

ENV APP_ENV=production \
    HOST=0.0.0.0 \
    PORT=80 \
    PYTHONPATH="$PYTHONPATH:/usr/src/app/src"

WORKDIR /usr/src/app
CMD ["python3", "src/run.py"]

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . /usr/src/app

