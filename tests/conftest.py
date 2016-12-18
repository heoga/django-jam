import os
import sys


def find_phantomjs():
    phantom = os.environ.get('PHANTOMJS')
    if phantom:
        return phantom
    path_options = os.environ.get('PATH', '').split(os.pathsep)
    for path in path_options:
        for name in ('phantomjs', 'phantomjs.exe'):
            candidate = os.path.join(path, name)
            if os.path.exists(candidate):
                return candidate


def pytest_configure(config):
    os.system('coverage erase')
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    # Setup.py doesn't play nice with the paths on Windows adding both normal
    # and lower case versions.  This means that when Django tries to import it
    # sees 'two' valid paths and exits.  This should work around that.
    lower_case = os.path.abspath(__file__).lower()
    if (
        lower_case != os.path.abspath(__file__)
    ) and os.path.exists(lower_case):
        sys.path = [a.lower() for a in sys.path]
    from django.conf import settings

    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    settings.configure(
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'DIRS': [],
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        MIDDLEWARE_CLASSES=MIDDLEWARE,
        INSTALLED_APPS=(
            'polymorphic',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'nimble.apps.NimbleConfig',
            'rest_framework',
            'bootstrap3',
            'tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
    )

    # guardian is optional
    try:
        import guardian  # NOQA
    except ImportError:
        pass
    else:
        settings.ANONYMOUS_USER_ID = -1
        settings.AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'guardian.backends.ObjectPermissionBackend',
        )
        settings.INSTALLED_APPS += (
            'guardian',
        )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
    # Now configure PhantomJS
    if config.option.driver is None:
        config.option.driver = 'PhantomJS'
        config.option.driver_path = find_phantomjs()
    # Clear flake8 & isort caches.
    for package in ('flake8', 'isort'):
        mtimes = os.path.join('.cache', 'v', package, 'mtimes')
        if os.path.exists(mtimes):
            os.remove(mtimes)


def pytest_unconfigure():
    os.system('coverage html')
