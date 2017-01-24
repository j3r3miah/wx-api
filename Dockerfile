FROM ubuntu:latest
MAINTAINER Jeremiah Boyle "jeremiah.boyle@gmail.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -yq        \
    python3                    \
    python3-pip                \
    uwsgi-plugin-python3       \
    postgresql-client          \
    libpq-dev                  \
    nginx                      \
    supervisor

# this upgrades pip, installing it as `pip` instead of `pip3`
RUN pip3 install --upgrade pip

COPY app/requirements.txt /var/www/app/requirements.txt
RUN pip install -r /var/www/app/requirements.txt

COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/log/app /var/www/app &&          \
    chown -R www-data:www-data /var/www/app &&     \
    chown -R www-data:www-data /var/log

WORKDIR /var/www/app

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
