SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "polls",
    "tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

#urlpatterns = []

TEMPLATE_CONTEXT_PROCESSORS = [
]
