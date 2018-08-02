FROM python:2.7

# TODO: remove this once we're happy it's working
RUN apt-get update && apt-get install -y \
    vim

# the 2.7 image seems to be a bit behind
RUN pip install --upgrade pip

# TODO: reduce this to just the folders we need
COPY . mqttwarn

RUN pip install -r mqttwarn/requirements-release.txt
RUN pip install -r mqttwarn/requirements-optional.txt

RUN pip install -e mqttwarn

# expect this folder to be volume-mounted and expect to find the config file there
VOLUME /etc/mqttwarn
ENV MQTTWARNINI /etc/mqttwarn/mqttwarn.ini

# run the app
CMD mqttwarn

