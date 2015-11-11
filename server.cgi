import os
APP_DIR=os.path.dirname(os.path.realpath(__file__))

# Activate the virtualenv
activate_this = APP_DIR + '/.virtualenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Add the application to the sys path
import sys
sys.path.insert(0, APP_DIR)

from app import app as application
