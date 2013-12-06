import os
from flask import Flask, request, url_for, abort, redirect, send_from_directory, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from helpers import is_valid_url, generate_code
import re
from datetime import datetime

# App
app = Flask(__name__)
if os.getenv('FLASK_ENV') is 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Database
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

# Routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def shorten():
    if request.method == 'GET':
        return render_template('hello.html')
    else:
        url = request.form['url'].strip()

        if not is_valid_url(url):
            abort(400)

        # Has this URL been previously stored?
        row = db.session.query(Urls).\
                        filter(Urls.url == url).\
                        first()
        if not row:
            code = generate_code()
            row = Urls(url=url, code=code)
            db.session.add(row)
            db.session.commit()

        return url_for('bounce', code=row.code, _external=True)

@app.route('/<code>', methods=['GET'])
def bounce(code):
    # Strip off any file extension
    code = re.sub(r'\.[a-zA-Z0-9]{1,5}$', '', code)

    row = db.session.query(Urls).\
                    filter(Urls.code == code).\
                    first()

    if not row:
        abort(404)

    row.clicks += 1
    db.session.add(row)
    db.session.commit()

    return redirect(row.url)

@app.route('/list', methods=['GET'])
def list():
    urls = db.session.query(Urls).\
                     order_by(Urls.created).\
                     all()

    return render_template('list.html', urls=urls)

if __name__ == '__main__':
    app.run('0.0.0.0')
