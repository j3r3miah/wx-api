
all: build

build:
	rm -f app/uwsgi.sock # lingering socket from killed uwsgi breaks build
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

rmlogs:
	rm -fr log/*.log
