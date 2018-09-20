FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y python-pip

# somehow apt-get installs an old version
RUN pip install --upgrade pip

RUN pip install jinja2
RUN pip install paho-mqtt
RUN pip install requests

RUN pip install mock
RUN pip install pytest

RUN apt-get install -y libmysqlclient-dev
RUN pip install MYSQL-python

WORKDIR /src

ENTRYPOINT bash

