try:
    import cPickle as pickle
except ImportError:
    import pickle
import sys
import traceback
from datetime import datetime
from pprint import pformat
from zlib import compress, decompress

from django.utils.hashcompat import sha_constructor
from django.template.defaultfilters import date, time
from django.http import HttpRequest

import settings

class AttrDict(HttpRequest,dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
            
def is_hex(s):
    if not s:
        return False
    for c in s:
        if c not in '0123456789abcdef':
            return False
    return True

def request2dict(request, exception, sha):
    obj_dict = dict([(k,{}) for k in ('REQUEST','GET','POST','FILES','COOKIES')])
    obj_dict.update(request.__dict__.copy(),
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
    if 'wsgi.input' in obj_dict['META']:
        del obj_dict['META']['wsgi.errors'], obj_dict['META']['wsgi.input']
    return obj_dict


def log_report(request):
    ctx = {}
    for k,v in request.items():
        if k.isupper():
            ctx[k] = pformat(v)
        else:
            ctx[k] = v
    settings.LOG_FILE.write(settings.LOG_FORMAT % ctx)
 	            #(pformat(request.GET), pformat(request.POST), pformat(request.COOKIES),
 	            #pformat(request.META), request.exception))
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
    seed = exception
    if settings.UNIQUE:
        seed = seed[1:-1]
    return sha_constructor(''.join(seed)).hexdigest(), '\n'.join(exception)
