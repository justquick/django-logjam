try:
    import cPickle as pickle
except ImportError:
    import pickle
import sys
import re
import traceback
from datetime import datetime
from pprint import pformat
from zlib import compress, decompress
from django.core.cache import get_cache
from django.utils.hashcompat import sha_constructor
from django.template.defaultfilters import date, time
from django.http import HttpRequest
import settings


cache = get_cache(settings.CACHE)
sha_re = re.compile(r'[a-f0-9]{40}')
ctrl = '%s%s' % (settings.PREFIX, 'ctrl')


class AttrDict(HttpRequest,dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
            

def request2dict(request, exception, sha):
    obj_dict = dict(
	GET = request.GET,
	POST = request.POST,
	FILES = request.FILES,
	COOKIES = request.COOKIES,
	META = request.META,
        id = sha,
        exception = exception,
        path = request.path,
        method = request.method,
        host = request.get_host(),
        is_ajax = request.is_ajax(),
        is_secure = request.is_secure(),
        encoding = request.encoding,
        timestamp = datetime.now(),
    )
    for key in ('wsgi.errors','wsgi.input','wsgi.file_wrapper'):
	if key in obj_dict['META']:
	    del obj_dict['META'][key]
    return obj_dict


def log_report(request):
    ctx = {}
    for k,v in request.items():
        if k.isupper():
            ctx[k] = pformat(v)
        else:
            ctx[k] = v
    settings.LOG_FILE.write(settings.LOG_FORMAT % ctx)
    settings.LOG_FILE.flush()

def deserialize(s):
    if settings.COMPRESS:
        s = decompress(s)
    return pickle.loads(s)

def serialize(request):
    val = pickle.dumps(request, -1)
    if settings.COMPRESS:
        return compress(val, settings.COMPRESS)
    return val

def format_exception(exc_info=None):
    exception = traceback.format_exception(*(exc_info or sys.exc_info()))
    seed = settings.UNIQUE and exception[1:-1] or exception 
    return sha_constructor(''.join(seed)).hexdigest(), '\n'.join(exception)
