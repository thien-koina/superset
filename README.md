# superset
Using SuperSet to build Visualization Tool

config.py is default config of superset download from https://github.com/apache/superset/blob/master/superset/config.py
env SUPERSET_HOME
env FLASK_ENV
env SUPERSET_FEATURE_*
env MAPBOX_API_KEY
env SUPERSET_CONFIG_PATH

```
# Setup
sudo apt install libpq-dev # if fatal error: libpq-fe.h: No such file or directory when install psypopg2

# Activate
. venv/bin/activate

export FLASK_APP=superset
export SUPERSET_HOME=./ # change to absolute path
export FLASK_ENV="development"
export CLIENT_ID=...
export CLIENT_SECRET=...
export DOMAIN=...

# init db
superset db upgrade
# Create an admin user (you will be prompted to set a username, first and last name before setting a password)
superset fab create-admin

# Load some data to play with
superset load_examples

# Create default roles and permissions
superset init

# To start a development web server on port 8088, use -p to bind to another port
superset run -p 8088 --with-threads --reload --debugger

# Deactivate
deactivate
```