FROM python:2.7

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y sudo

RUN pip install --upgrade pip

## build /opt/mqttwarn
#RUN mkdir -p /opt/mqttwarn
#WORKDIR /opt/mqttwarn
#
### add user mqttwarn to image
##RUN groupadd -r mqttwarn && useradd -r -g mqttwarn mqttwarn -p '*'
##RUN usermod -aG sudo mqttwarn
##RUN chown -R mqttwarn /opt/mqttwarn
##
### process run as mqttwarn user
##USER mqttwarn
#

# finally, copy the current code (ideally we'd copy only what we need, but it
#  is not clear what that is, yet)
COPY . /opt/mqttwarn

RUN pip install -e /opt/mqttwarn

VOLUME ["/etc/mqttwarn"]
ENV MQTTWARNINI="/etc/mqttwarn/mqttwarn.ini"

# run process
CMD mqttwarn

