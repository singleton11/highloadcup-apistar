FROM python:3.6.2-alpine3.6

RUN pip install pipenv

WORKDIR /home/app

RUN apk --no-cache add gcc musl-dev linux-headers

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system

COPY . .

CMD ["./bootstrap.sh"]