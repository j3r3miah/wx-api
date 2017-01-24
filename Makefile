
all: build up

build: down clean_up_after_uwsgi
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean_up_after_uwsgi:
	rm -f app/uwsgi.sock

clean:
	rm -fr log/*.log db/*
