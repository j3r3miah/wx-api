# Flask Skeleton Environment

- Python 3.5
- PostgreSQL
- uWSGI
- nginx
- Alembic

### Requirements

- Docker (I'm using 1.13.0 on Mac)
- Docker Compose

### Instructions

Firstly, get the postgres db volume set up: `$ make db_init`

Build the containers: `$ make build`

Start everything up: `$ make up`

Tail the logs: `$ make logs`

If uWSGI gets jammed: `$ make bounce`

Stop everything: `$ make down`

Take a look at the  Makefile for other commands.
