from idiocy.app import app
import os
import re
from flask import abort, \
                  redirect, \
                  render_template, \
                  request, \
                  send_from_directory, \
                  url_for
from idiocy.helpers import generate_code, \
                           is_valid_url
from idiocy.database import db, \
                            Urls
from idiocy.filters import strip_www

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def shorten():
    if request.method == 'GET':
        return render_template('hello.html')
    else:
        api_key = request.headers['Authorization'].strip()
        if api_key != app.config['API_KEY']:
            abort(403)

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

        return strip_www(url_for('bounce', code=row.code, _external=True))

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
