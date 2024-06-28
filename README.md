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

## Reference

* <https://www.youtube.com/watch?v=G1FBSYJ45Ww>
