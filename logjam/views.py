from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from client import Client
from datetime import datetime
from time import strptime
from util import prefix, cache
import settings
import os

from models import HttpException


parse_date = lambda s: datetime(*strptime(s, '%m/%d/%Y')[:3])

def admin(request):
    f = request.REQUEST.get('from', '')
    t = request.REQUEST.get('to', '')
    p = int(request.REQUEST.get('page', 1))
    d = int(request.REQUEST.get('display', 50))
    errors = list(Client().get_all())
    if f:
        errors = filter(lambda e: e['timestamp'] > parse_date(f), errors)
    if t:
        errors = filter(lambda e: e['timestamp'] <= parse_date(t), errors)
    errors.reverse()
    return render_to_response('logjam/admin.html', {
        'errors': errors[d*(p-1):d*p],
    },context_instance=RequestContext(request))

def archive(request, sha):
    obj = Client().get(sha)
    HttpException.objects.create(
 	GET = repr(obj['GET']),
	POST = repr(obj['POST']),
	FILES = repr(obj['FILES']),
	COOKIES = repr(obj['COOKIES']),
	META = repr(obj['META']),
        sha = sha,
        exception = obj['exception'],
        path = obj['path'],
        method = obj['method'],
        host = obj['host'],
        is_ajax = obj['is_ajax'],
        is_secure = obj['is_secure'],
        encoding = obj['encoding'] or 'utf8',
        timestamp = obj['timestamp'])
    cache.delete(prefix(sha))
    return HttpResponse('The exception has been archived in database')