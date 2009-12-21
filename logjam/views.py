from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.cache import cache
from client import Client
from datetime import datetime
from time import strptime
from util import prefix, cache as appcache
import settings
import os

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
    cache.set(prefix(sha), Client().get(sha))
    appcache.delete(prefix(sha))
    return HttpResponse()