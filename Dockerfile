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

# get this pip stuff done and cached early because it is slow

COPY app/requirements.txt /var/www/app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /var/www/app/requirements.txt

# now iteration on config doesn't invalidate cached pip install

COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/log/app && \
    rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf && \
    chown -R www-data:www-data /var/www/app && \
    chown -R www-data:www-data /var/log

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
