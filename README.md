# superset
Using SuperSet to build Visualization Tool

# Note
config.py is default config of superset download from https://github.com/apache/superset/blob/master/superset/config.py

```
# Setup
sudo apt install libpq-dev # if fatal error: libpq-fe.h: No such file or directory when install psypopg2

# Setup Environment Variables
export SUPERSET_HOME=~/Documents/superset/
export PYTHONPATH=~/Documents/superset/
export FLASK_APP=superset
export FLASK_ENV="development"
export CLIENT_ID="..."
export CLIENT_SECRET="..."
export DOMAIN="koina.vn"

# Activate
source env/bin/activate

# Init Database
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

# Bugs:
1. Google OAuth always auto pass through consent screen (not show to help user chooses another one)