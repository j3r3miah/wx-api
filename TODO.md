
- Just get this into a usable state a driver for a command line monitoring tool
- Then deploy it somewhere. Then continue to improve it incrementally.


## WX-API ##

- How the F do you get flask route wildcards or webargs or whatever for spot_id?
- Finalize data model

## ScraperService ##

- Read spots in bg/async and log to database
  - Reading spot starts timer task which refreshes the spot at random interval
  - If spot is not read for a given interval, discontinue timer task
- We actually do want some concurrency. We want to be able to get a status
  update from the service while longer running tasks are in progress. We just
  need synchronization around the webdriver. How do we do that?
  - Can I just enable 2 workers and ensure by convention that top level tasks
    never block? That way we have one worker available for bg processing. But
    how do you prevent both workers getting hung up doing long running tasks?
      - Only one task which uses webdriver can be executed at a time.
        - Make them all synchronous subtasks of a singleton task? Better way?
          - Separate queues!: `@worker.task(queue='webdriver_queue')`
      ★ Ensuring a task is only executed one at a time: https://goo.gl/7thMC9


- How best to present the worker API? Instead of random methods, a class?
  - Commands typically produce session state (login) or write web results to db
  - Async notification of updates not needed until later (polling => webhooks)

- How do I cancel/interrupt and reset driver when webpage gets jammed?

## Scraper ##

- Capture wind meter and wind speed graph images
- Handle invalid/NotFound `spot_id`
  - Catch all webdriver exceptions and wrap in something sensible
  - Include the inner exception so that it's easier to debug from API app?
- Leverage Chrome fast refreshing via webdriver?
  - Does refresh do it? Does loading the same URL that is already loaded do it?
  - If so, keep a tab open per spot which we are monitoring (hash on `spot_id`)

## DevOps ##

Deploy
  - Give postgres a proper password and get it out of the source code.
  - Kill VNC exposure before deploy!
  - Deploy to AWS free tier

- I am in dependency hell between these two applications. Right now they share
  a session and the service depends on Flask and the Flask app autoreloads when
  the service code changes :( What's the simplest solution?
  - Separate completely with shared packages for models
    - Can't use Flask-SQLAlchemy then... but perhaps that's better

- Clean up file tree organization, module naming, etc
  - `app`/`service` or `api`/`scraper`?
- Clean up requirements for service vs api images
- Rename `app` (dir and module) to api?
- Rename `base` to `scraper`

- Upgrade python packages

- Why doesn't PDB work with docker? I have `stdin_open` and `tty` in
  docker-compose.yml. Will PDB ever work in Celery?
