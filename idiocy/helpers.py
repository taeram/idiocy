from rfc3987 import parse
import string
import random
import re

def is_valid_url(url):
   p = parse(url, rule='URI_reference')
   return all([p['scheme'], p['authority']])

def generate_code(length=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))

def is_authenticated(app_api_key, request_api_key):
    return app_api_key == request_api_key.strip()

def strip_file_extension(url):
    return re.sub(r'\.[a-zA-Z0-9]{1,5}$', '', url)

