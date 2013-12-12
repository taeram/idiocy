import os
from flask import Flask

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if os.getenv('FLASK_ENV') is 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

import idiocy.views
import idiocy.filters