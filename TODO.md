
## DevOps ##

- I am in dependency hell between these two applications. Right now they share
  a session and the service depends on Flask and the Flask app autoreloads when
  the service code changes :( What's the simplest solution?
  - Join everything into one app
  - Separate completely with shared packages for models
    - Can't use Flask-SQLAlchemy then... but perhaps that's better

- Clean up file tree organization, module naming, etc
  - `app`/`service` or `api`/`scraper`?
- Clean up requirements for service vs api images
- Rename `app` (dir and module) to api?
- Rename `base` to `scraper`
- Why doesn't PDB work with docker? I have `stdin_open` and `tty` in
  docker-compose.yml.

Before Deploy:
  - Give postgres a proper password and get it out of the source code.
  - Kill VNC exposure before deploy!
  - Upgrade python packages

Where should I run this?
  - Run on seedbox? No docker support
    - Could still install into my shell account... kinda lame/insecure
  - Learn about a new (free?) docker container hosting service
    - Docker Swarm, Kubernetes, etc: https://goo.gl/bWfPFM (ebook)
    - Probably none of these are free
  - AWS free tier? I'm sure an image which supports docker is available.
    - This is probably the best idea
  - "Now" looks really cool. Pricing? https://goo.gl/1zuGVQ

## WX-API ##

- Create data model
  - WX is responsible for creating and migrating the DB schema
  - Models are Flask-SQLAlchemy based and live in a shared package
  - Service depends requires Flask deps to use models but can leverage model
    implementation shared with API.
  - Service could use raw SQLAlchemy to manage its state table because that
    doesn't need to be exposed in the models package.

## ScraperService ##

- How do I talk to the db from the service?

- We actually do want some concurrency. We want to be able to get a status
  update from the service while longer running tasks are in progress. We just
  need synchronization around the webdriver. How do we do that?

- How best to present the worker API? Instead of random methods, a class?
  - Commands typically produce session state (login) or write web results to db
  - Async notification of updates not needed until later (polling => webhooks)

- Read spots in bg/async and log to database
  - Reading spot starts timer task which refreshes the spot at random interval
  - If spot is not read for a given interval, discontinue timer task

- How do I cancel/interrupt and reset driver when webpage gets jammed?

## Scraper ##

- Capture wind meter and wind speed graph images
- Handle invalid/NotFound `spot_id`
  - Catch all webdriver exceptions and wrap in something sensible
  - Include the inner exception so that it's easier to debug from API app?
- Leverage Chrome fast refreshing via webdriver?
  - Does refresh do it? Does loading the same URL that is already loaded do it?
  - If so, keep a tab open per spot which we are monitoring (hash on `spot_id`)
