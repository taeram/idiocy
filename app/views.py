from app import app
import os
from flask import abort, \
                  redirect, \
                  render_template, \
                  request, \
                  send_from_directory, \
                  url_for
from helpers import generate_code, \
                    is_valid_url, \
                    is_authenticated, \
                    strip_file_extension
from database import db, \
                     Urls
from filters import strip_www


@app.route('/.well-known/acme-challenge/<filename>')
def letsencrypt(filename):
    return send_from_directory(os.path.join(app.root_path, '../.well-known/acme-challenge/'), filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def shorten():
    if request.method == 'GET':
        return render_template('hello.html')
    elif request.method == 'POST':
        if not is_authenticated():
            return app.response_class(response='{"error": "Invalid API key"}', mimetype='application/json', status=403)

        url = request.form['url'].strip()
        if not is_valid_url(url):
            return app.response_class(response='{"error": "Invalid URL"}', mimetype='application/json', status=403)

        # Has this URL been previously stored?
        row = db.session.query(Urls).\
                        filter(Urls.url == url).\
                        first()
        if not row:
            row = Urls(url=url, code=generate_code())
            db.session.add(row)
            db.session.commit()

        return strip_www(url_for('bounce', code=row.code, _external=True))

@app.route('/<code>', methods=['GET', 'DELETE'])
def bounce(code):
    code = strip_file_extension(code)
    row = db.session.query(Urls).\
                    filter(Urls.code == code).\
                    first()

    if not row:
        abort(404)

    if request.method == 'GET':
        row.clicks += 1
        db.session.add(row)
        db.session.commit()
        return redirect(row.url)

    elif request.method == 'DELETE':
        db.session.delete(row);
        db.session.commit()

        return strip_www(url_for('bounce', code=row.code, _external=True))

@app.route('/list', methods=['GET'])
def list():
    urls = db.session.query(Urls).\
                     order_by(Urls.created).\
                     limit(25).\
                     all()

    return render_template('list.html', urls=urls)
