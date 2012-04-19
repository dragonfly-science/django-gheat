import os
from fabric.api import sudo, cd, local, env, run, lcd, get, settings, put, prefix


#### Begin env settings ####

env.user = 'gheat'
env.repo = 'git@github.com:dragonfly-science/django-gheat.git'
env.sitename = 'gheat'
env.local_path = os.getcwd()
env.postgres = '8.4'

def packages():
    local('sudo apt-get install memcached')
    local('sudo apt-get install postgresql-%(postgres)s-postgis' % env)

def drop_db():
    local('dropdb gheat')
    local('dropuser gheat')

def make_db():
    local('createuser -S -d -r gheat')
    local('createdb gheat -O gheat')
    local('createlang plpgsql gheat')
    local('psql -d gheat -U gheat -f /usr/share/postgresql/%(postgres)s/contrib/postgis.sql' % env)
    local('psql -d gheat -U gheat -f /usr/share/postgresql/%(postgres)s/contrib/spatial_ref_sys.sql' % env)
    local("psql gheat -c 'grant all on spatial_ref_sys to gheat'")
    local("psql gheat -c 'grant all on geometry_columns to gheat'")

def django_syncdb():
    with prefix("source /usr/local/bin/virtualenvwrapper.sh && workon summaryweb"):
        local('pip install -r ../../requirements.txt')
        local('python manage.py syncdb')


