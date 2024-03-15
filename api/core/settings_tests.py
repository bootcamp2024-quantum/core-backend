from .settings import *  # noqa

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
SOUTH_TESTS_MIGRATE = False