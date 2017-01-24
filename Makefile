
all: build up

build: down _clean_up_after_uwsgi
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

psql: _db_start
	docker-compose run --rm -e PGPASSWORD=password base \
	    psql -h db -U postgres app_dev

db_init: _rm_db _db_first_start
	docker-compose run --rm -e PGPASSWORD=password base \
	    psql -h db -U postgres -c 'CREATE DATABASE app_dev;'
	docker-compose run --rm base python3 manage.py db init
	docker-compose run --rm base python3 manage.py db migrate
	docker-compose run --rm base python3 manage.py db upgrade

db_migrate: _db_start
	docker-compose run --rm base python3 manage.py db migrate

db_upgrade: _db_start
	docker-compose run --rm base python3 manage.py db upgrade

clean: _rm_logs _rm_db


_clean_up_after_uwsgi:
	rm -f app/uwsgi.sock

_rm_db:
	rm -fr db/*

_rm_logs:
	rm -fr log/*.log

_db_start:
	docker-compose up -d db && sleep 2

_db_first_start:
	docker-compose up -d db && sleep 20
