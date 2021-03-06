import os

# Googlemaps api key
try:
    from secrets import GOOGLEMAPS_API_KEY
except ImportError:
    GOOGLEMAPS_API_KEY = ''


PROJECT_HOME = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Replace this with your own PostGIS (or other GeoDjango-ready) database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gheat',
        'USER': 'gheat',
        'HOST': '127.0.0.1'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/gmap/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL= '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2!8+e=g^cm@6kc2xq3(d#5sp#$jgmpit5ma!_^89ho1*h5po@6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_HOME, 'templates'),
)

INSTALLED_APPS = (
    'gmap',
    'gheat',
)

# ===== gheat specific settings =====
# see gheat.default_settings for a full list of settings you can override

GHEAT_MAP_MODE_SUM_DENSITY = 1001
STORAGE_FILESYSTEM = 1

GHEAT_ALWAYS_BUILD = False
GHEAT_FILESYSTEM_STORAGE_DIR = '/tmp/gheat/'

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        }
#}

GHEAT_STORAGE_BACKEND = STORAGE_FILESYSTEM
GHEAT_RENDER_BACKEND = 'Numeric'
GHEAT_MAX_VALUE = 7
GHEAT_SCALING_COEFFICIENT =  1
GHEAT_MAP_MODE = GHEAT_MAP_MODE_SUM_DENSITY
GHEAT_MIN_DENSITY = 0.1

