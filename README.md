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

Firstly, get the postgres db volume set up: `$ ./develop init_db`

Build the containers: `$ ./develop build`

Start everything up: `$ ./develop up`

Tail the logs: `$ ./develop logs`

If uWSGI gets jammed: `$ ./develop bounce`

Stop everything: `$ ./develop down`

Take a look at the `develop` for other commands.
