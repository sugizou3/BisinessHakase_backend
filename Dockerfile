FROM python:3.9.7

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install -r requirements.txt
