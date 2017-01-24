
all: build up

build: down _clean_up_after_uwsgi
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

db_start:
	docker-compose start db

psql:
	# docker-compose start db && sleep 2
	docker-compose run --rm -e PGPASSWORD=password base \
	    psql -h db -U postgres app_dev
	# docker-compose stop db

db_init:
	# docker-compose start db && sleep 2
	docker-compose run --rm base \
	    python3 manage.py db init
	# docker-compose stop db

db_migrate:
	# docker-compose start db && sleep 2
	docker-compose run --rm base \
	    python3 manage.py db migrate
	# docker-compose stop db

db_upgrade:
	# docker-compose start db && sleep 2
	docker-compose run --rm base \
	    python3 manage.py db upgrade
	# docker-compose stop db

clean:
	rm -fr log/*.log db/*

_clean_up_after_uwsgi:
	rm -f app/uwsgi.sock
