# Superset specific config
ROW_LIMIT = 50000

SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
# Your App secret key
SECRET_KEY = "\2\1thisismyscretkey\1\2\\e\\y\\y\\h"

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# SQLALCHEMY_DATABASE_URI = "sqlite:////path/to/superset.db"
# setup env SUPERSET_HOME to change SQLALCHEMY_DATABASE_URI path

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
# WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
# WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
# MAPBOX_API_KEY = ""

# OAuth2
import os
from flask_appbuilder.security.manager import (
    AUTH_OID,
    AUTH_REMOTE_USER,
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)

# This will make sure the redirect_uri is properly computed, even with SSL offloading
ENABLE_PROXY_FIX = True

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        "name": "google",
        "icon": "fa-google",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "api_base_url": "https://www.googleapis.com/oauth2/v2/",
            "client_kwargs": {"scope": "email profile"},
            "request_token_url": None,
            "access_token_url": "https://accounts.google.com/o/oauth2/token",
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "authorize_params": {"hd": os.getenv("DOMAIN")},
        },
    }
]

# Map Authlib roles to superset roles
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"

# Will allow user self registration, allowing to create Flask users from Authorized User
AUTH_USER_REGISTRATION = False

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin"


from custom_sso_security_manager import CustomSsoSecurityManager

CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
