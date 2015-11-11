from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, prompt_bool
from datetime import datetime

db = SQLAlchemy(app)

manager = Manager(usage="Manage the database")

@manager.command
def create():
    "Create the database"
    db.create_all()

@manager.command
def drop():
    "Empty the database"
    if prompt_bool("Are you sure you want to drop all tables from the database?"):
        db.drop_all()

@manager.command
def recreate():
    "Recreate the database"
    drop()
    create()

class Urls(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.VARCHAR(length=255), unique=True)
    code = db.Column(db.VARCHAR(length=255), unique=True)
    clicks = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, url, code):
        self.url = url
        self.code = code

    def __repr__(self):
        return "<Url ('%r', '%r')>" % (self.url, self.code)
