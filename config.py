import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEVELOPMENT = False
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
    SCRAPER_DATA_DIR = os.environ['SCRAPER_DATA_DIR']
    WEBSITE_CREDENTIALS = os.environ['WEBSITE_CREDENTIALS']
    WEBSITE_URLS = os.environ['WEBSITE_URLS']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
