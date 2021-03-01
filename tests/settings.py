SECRET_KEY = "tests!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

INSTALLED_APPS = ["tests"]
