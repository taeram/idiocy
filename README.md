Idiocy
======

Idiocy is a Python powered URL shortening service.

Requirements
============
You'll need the following:

* [Python 3](http://www.python.org/)
* [pip](https://github.com/pypa/pip)
* [Virtualenv](https://github.com/pypa/virtualenv)

Setup
=====
Local development setup:
```bash
    # Clone the repo
    git clone https://github.com/taeram/idiocy.git

    cd ./idiocy/

    # Setup and activate virtualenv
    virtualenv .venv
    source ./.venv/bin/activate

    # Install the pip requirements
    pip install -r requirements.txt

    # Create the development database (SQLite by default)
    python manage.py database create

    # Start the application, prefixing with the required environment variables
    API_KEY="secret_api_key" python main.py
```

Usage
=====

To shorten a URL, POST it to http://your-domain.com using your API key:

```bash
curl -X POST http://your-domain.com -H "Authorization: secret_api_key" -F "url=http://example.com/kitty.gif"
```

The body of the response will contain the shortened URL:

```bash
http://your-domain.com/oT0Dh
```

Some services will generate image previews of an image URL if it has the
correct file extension. To enable this, simply add a file extension to the
shortened URL:

```bash
http://your-domain.com/oT0Dh.gif
```

To remove a URL, simply DELETE it using its short URL:

```bash
curl -X DELETE http://your-domain.com/oT0Dh -H "Authorization: secret_api_key"
```
