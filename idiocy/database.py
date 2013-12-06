from idiocy.app import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Urls(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True)
    code = db.Column(db.Text, unique=True)
    clicks = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, url, code):
        self.url = url
        self.code = code

    def __repr__(self):
        return "<Url ('%r', '%r')>" % (self.url, self.code)

db.create_all()
