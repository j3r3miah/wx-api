FROM selenium/node-chrome-debug:3.5.3
MAINTAINER Jeremiah Boyle "jeremiah.boyle@gmail.com"

USER root

ENV DEBIAN_FRONTEND noninteractive

# pdbpp requires UTF-8 and it's generally saner than the posix default
ENV LANG C.UTF-8

RUN apt-get update
RUN apt-get install -yq        \
    python3                    \
    python3-pip                \
    uwsgi-plugin-python3       \
    libpq-dev

# this upgrades pip, installing it as `pip` instead of `pip3`
RUN pip3 install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY uwsgi/uwsgi.ini /etc/uwsgi.ini

WORKDIR /wx-api

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi.ini"]
