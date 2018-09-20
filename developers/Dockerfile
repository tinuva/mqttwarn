FROM python:2.7

# this image has an old version of pip
RUN pip install --upgrade pip

RUN pip install jinja2
RUN pip install mock
RUN pip install MYSQL-python
RUN pip install paho-mqtt
RUN pip install pytest
RUN pip install requests

WORKDIR /src

ENTRYPOINT bash

