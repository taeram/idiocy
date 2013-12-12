from idiocy.app import app
import re

@app.template_filter('strip_www')
def strip_www(url):
    if app.config['STRIP_WWW_PREFIX']:
        url = url.replace('www.', '')

    return url

@app.template_filter('strip_scheme')
def strip_scheme(url):
    return re.sub('^.*://', '', url)
