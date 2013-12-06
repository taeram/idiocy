from rfc3987 import parse
import string
import random

def is_valid_url(url):
   p = parse(url, rule='URI_reference')
   return all([p['scheme'], p['authority']])

def generate_code(length=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))
