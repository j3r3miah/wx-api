FROM ubuntu:latest
MAINTAINER Jeremiah Boyle "jeremiah.boyle@gmail.com"

WORKDIR /var/www/app

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -yq        \
    python3                    \
    python3-pip                \
    uwsgi-plugin-python3       \
    libpq-dev

# this upgrades pip, installing it as `pip` instead of `pip3`
RUN pip3 install --upgrade pip

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY uwsgi/uwsgi.ini /etc/uwsgi.ini

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi.ini"]
