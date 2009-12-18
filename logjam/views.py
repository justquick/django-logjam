from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from client import Client
from datetime import datetime
from time import strptime
from util import cache

client = Client()
parse_date = lambda s: datetime(*strptime(s, '%m/%d/%Y')[:3])

def admin(request):
    f = request.REQUEST.get('from', '')
    t = request.REQUEST.get('to', '')
    p = int(request.REQUEST.get('page', 1))
    d = int(request.REQUEST.get('display', 5))
    errors = map(client.get, list(client.all()))
    if f:
        errors = filter(lambda e: e['timestamp'] > parse_date(f), errors)
    if t:
        errors = filter(lambda e: e['timestamp'] <= parse_date(t), errors)
    return render_to_response('logjam/admin.html', {
        'errors': errors[d*(p-1):d*p],
    },context_instance=RequestContext(request))

def archive(request, sha):
    client.get(sha)
    cache.delete(sha)
    return HttpResponse()