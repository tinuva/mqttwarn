FROM python:2.7-alpine

# based on https://github.com/pfichtner/docker-mqttwarn

# install python libraries by various methods
RUN apk update
RUN apk add \
        gcc \
        git \
        gobject-introspection \
        libc-dev \
        libffi-dev \
        librrd \
        openssl-dev \
        python-dev \
        py-mysqldb \
        rrdtool \
        rrdtool-dev

RUN pip install \
        #azure-iothub-device-client \
        dnspython \
        fbchat==v1.4.0 \
        git+https://github.com/Azelphur/pyPushBullet.git \
        google-api-python-client \
        gspread \
        jinja2 \
        Mastodon.py \
        paho-mqtt \
        pgi \
        puka \
        pyserial \
        pyst2 \
        python-twitter \
        rrdtool \
        redis \
        requests \
        slacker \
        twilio \
        websocket-client

RUN easy_install \
        apns \
        Pastebin


ENV MQTT_HOME=/opt/mqttwarn

# we'll put the source here
RUN mkdir -p $MQTT_HOME
WORKDIR $MQTT_HOME

# add user 'mqttwarn' and give them control of the folder
RUN addgroup -S mqttwarn && adduser -D -S mqttwarn -G mqttwarn
RUN chown -R mqttwarn $MQTT_HOME

# switch the user
USER mqttwarn

# expect this folder to be volume mounted
VOLUME ["$MQTT_HOME/conf"]

# set conf path
ENV MQTTWARNINI="$MQTT_HOME/conf/mqttwarn.ini"

# finally, copy the current code (ideally we'd copy only what we need, but it
#  is not clear what that is, yet)
COPY . $MQTT_HOME

# run process
CMD python mqttwarn.py

