from django.conf.urls.defaults import *

urlpatterns = patterns('logjam.views',
     (r'^$', 'admin'),
     (r'^(?P<sha>[a-f0-9]{40})$', 'archive'),
)
