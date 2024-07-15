""" This section of code is dedicated to establishing static and custom API routes.
Given that the '/admin' route is already occupied by Flask-Admin, an alternative
route '/adminapi' is introduced. This newly defined route '/adminapi' is utilized
to serve both static files and custom API endpoints through the admin blueprint.
For instance, to access the 'schema.png' file located within the static directory,
the following syntax can be used: "{{ url_for('adminapi.static', filename='static/schema.png') }}".
This approach ensures that our custom and static content is accessible without
conflicting with Flask-Admin's default routes.
"""
from flask import Blueprint
import os.path as op

path = op.join(op.dirname(__file__), 'adminapi', 'static')

adminapi_blueprint = Blueprint('adminapi', __name__,
                        static_folder=path,
                        static_url_path='/static')

# Add your routes and custom functions here
@adminapi_blueprint.route('/hello')
def admin_dashboard():
    return "Hello!"