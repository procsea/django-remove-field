test:
	DJANGO_SETTINGS_MODULE='tests.settings' poetry run django-admin test
	DJANGO_REMOVE_FIELD_DISABLED=1 DJANGO_SETTINGS_MODULE='tests.settings' poetry run django-admin test

makemigrations:
	DJANGO_SETTINGS_MODULE='tests.settings' DJANGO_REMOVE_FIELD_DISABLED=1 poetry run django-admin makemigrations