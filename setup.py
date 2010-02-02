from distutils.core import setup

setup(
    name = "django-logjam",
    version = '0.1',
    url = 'http://github.com/justquick/django-logjam',
    author = 'Justin Quick',
    description = 'Optimized error reporting for Django',
    packages = ['logjam','logjam.management','logjam.management.commands']
)
