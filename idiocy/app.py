import os
from flask import Flask

# App
app = Flask(__name__)
if os.getenv('FLASK_ENV') is 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

import idiocy.views
