import os
import sys
sys.path.insert(0, '/home/jquick/Projects/django-logjam')
sys.path.insert(0, '/home/jquick/Projects/django-logjam/test_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from logjam.handlers import WSGIHandler
application = WSGIHandler()