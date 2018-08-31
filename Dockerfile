FROM python:2.7

# TODO: remove this once we're happy it's working
RUN apt-get update && apt-get install -y \
    vim

# the 2.7 image seems to be a bit behind
RUN pip install --upgrade pip

RUN mkdir mqttwarn
COPY requirements-*.txt mqttwarn/

RUN pip install -r mqttwarn/requirements-release.txt
RUN pip install -r mqttwarn/requirements-optional.txt

#COPY assets mqttwarn/
#COPY etc mqttwarn/
#COPY examples mqttwarn/
#COPY mqttwarn mqttwarn/
#COPY mqttwarn.egg-info mqttwarn/
#COPY templates mqttwarn/
#COPY vendor mqttwarn/
#
#COPY Makefile mqttwarn/
#COPY MANIFEST.in mqttwarn/
#COPY setup.py mqttwarn/

COPY . mqttwarn/

RUN pip install -e mqttwarn

# expect this folder to be volume-mounted and expect to find the config file there
VOLUME /etc/mqttwarn
ENV MQTTWARNINI /etc/mqttwarn/mqttwarn.ini

# run the app
CMD mqttwarn

