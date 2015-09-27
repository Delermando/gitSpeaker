import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = "postgres://goppvwhsahqvlr:EJ7wGIxill234JW1z9PLsiPhFY@ec2-54-163-228-109.compute-1.amazonaws.com:5432/d5c7mhsq8h6jpl"
SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_GOLD_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


