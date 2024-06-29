# Admin Dashboard Plugin

See templates/admin/index.html for a description of this application.

## Installation

Create a new environment

`conda create -n your_env_name python==3.11`

Install the latest dependencies (preferred)

`pip install Flask-Admin Flask-Bootstrap SQLAlchemy Flask-SQLAlchemy python-dotenv WTForms-Components Flask-WTF`

If project does not work for some reason check requirements.txt which are the libraries this project is known to work with.

Create the schema.

```sh
flask shell

db.create_all()
exit()

flask run
```

## How to run

Navigate to: the url printed on the console /admin

## How to run on Server

Create a /etc/systemd/system/gunicorn.service file

```ini
[Unit]
Description=Gunicorn instance to serve your Flask application
After=network.target

[Service]
User=verma
Group=www-data
WorkingDirectory=/home/verma/flask/python_flask_admin
ExecStart=/bin/bash -c './venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 -w 4 wsgi:app'

[Install]
WantedBy=multi-user.target
```

Configure it as a service

```sh
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

sudo systemctl status gunicorn
```

### Configure Apache2 with new sub-domain

see: website-apache-setup.md

### Configure Apache2 with new sub-page

see: website-apache-setup.md

TODO: improve this by using ssl and also redirect 80 traffic to ssl.
TODO: try to get gunicorn to not bind to all addresses

## Reference

* <https://www.youtube.com/watch?v=G1FBSYJ45Ww>
