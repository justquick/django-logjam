from django.conf import settings
import sys

HOST = getattr(settings, 'LOGJAM_HOST', 'localhost')
PORT = getattr(settings, 'LOGJAM_PORT', 8001)
TIMEOUT = getattr(settings, 'LOGJAM_TIMEOUT', 5)
CACHE = getattr(settings, 'LOGJAM_CACHE_BACKEND', 'locmem:///')
LOG_FILE = getattr(settings, 'LOGJAM_LOG_FILE', sys.stdout)
LOG_FORMAT = getattr(settings, 'LOGJAM_LOG_FORMAT', '%(host)s - [%(timestamp)s] "%(method)s %(path)s" \n%(exception)s')
                     #'<ExceptionRequest\nGET:%(GET)s,\nPOST:%(POST)s,\nCOOKIES:%(COOKIES)s,\nMETA:%(META)s>\n\n%(exception)s\n')
PREFIX = getattr(settings, 'LOGJAM_CACHE_PREFIX', 'logjam_')
UNIQUE = getattr(settings, 'LOGJAM_UNIQUE', False)
PIDFILE = getattr(settings, 'LOGJAM_PIDFILE', '/tmp/logjam.pid')
DEBUG = getattr(settings, 'LOGJAM_DEBUG', True)
DAEMONIZE = getattr(settings, 'LOGJAM_DAEMONIZE', False)
COMPRESS = getattr(settings, 'LOGJAM_COMPRESSION', 5)