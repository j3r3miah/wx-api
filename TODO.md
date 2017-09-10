
## DevOps ##

- Clean up file tree organization, module naming, etc
- Rename `app` (dir and module) to api?
- Rename `base` to `scraper`

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

## WX-API ##


## ScraperService ##

- Scraper operations need to be async
  - Flask + Celery + AMQP
  - Flask + Redis Queue
    - Redis is worth learning
  - I think it would be sane to use Python threads for this
    - An experience with Python threads would be good

- Create `ScraperService` class that Flask talks to (instead of `Scraper`)
  - A single thread that manages the webdriver
  - Synchronized methods to enqueue commands
    - No results are necessary
  - Commands typically produce session state (login) or write web results to db
  - Async notification of updates not needed until later (polling => webhooks)
  - I am describing a Task Queue like Celery aren't I...

- Limit celery to one task: webdriver can only do one thing at a time
- But I need a way to cancel/interrupt and reset driver when it gets jammed

- Create data model
- Read spots in bg/async and log to database
- Flask endpoint just returns latest capture

## Scraper ##

- Does the page refresh on it's own? Maybe I can just "leave" it open
  - Async notification of page refreshes? Or must I poll the DOM?
  - Otherwise, make the refresh interval seem human-like
- Open spots in different "tabs" in same session?
- Capture wind meter and wind speed graph images
