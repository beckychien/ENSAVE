FROM python:3.6-stretch

RUN pip install django uwsgi;

COPY ./ENSAVE /ENSAVE
COPY ./requirements.txt /requirements.txt
WORKDIR /ENSAVE

RUN pip install -r /requirements.txt

EXPOSE 80
