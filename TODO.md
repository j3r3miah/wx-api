
## DevOps ##

- Why doesn't PDB work with docker? I have `stdin_open` and `tty` in
  docker-compose.yml.

- Give postgres a proper password and get it out of the source code.
- Kill VNC exposure before deploy!
- Upgrade python packages

- Where should I run this?
  - Run on seedbox? No docker support
    - Could still install into my shell account... kinda lame/insecure
  - Learn about a new (free?) docker container hosting service
    - Docker Swarm, Kubernetes, etc: https://goo.gl/bWfPFM (ebook)
    - Probably none of these are free
  - AWS free tier? I'm sure an image which supports docker is available.
    - This is probably the best idea
  - "Now" looks really cool. Pricing? https://goo.gl/1zuGVQ

## Service ##

- Scraper operations need to be async
  - Flask + Celery + AMQP
  - Flask + Redis Queue
    - Redis is worth learning
  - I think it would be sane to use Python threads for this
    - An experience with Python threads would be good

- Create data model
- Read spots in bg/async and log to database
- Flask endpoint just returns latest capture

## Scraper ##

- Capture wind meter and wind speed graph images
- Does the page refresh on it's own? maybe i can just "leave" it open
  - Otherwise, make the refresh interval seem human-like
- Open spots in different "tabs" in same session?
