FROM ubuntu:latest
MAINTAINER Jeremiah Boyle "jeremiah.boyle@gmail.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -yq        \
    python-pip                 \
    python-dev                 \
    uwsgi-plugin-python        \
    nginx                      \
    supervisor

COPY nginx/flask.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY app/requirements.txt /var/www/app/requirements.txt

RUN mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && pip install --upgrade pip \
    && pip install -r /var/www/app/requirements.txt \
    && chown -R www-data:www-data /var/www/app \
    && chown -R www-data:www-data /var/log

CMD ["/usr/bin/supervisord"]
