from django.conf.urls.defaults import *

urlpatterns = patterns('logjam.views',
     (r'^$', 'admin'),
     (r'^errors\.js$', 'errjs'),
     (r'^archive/(?P<sha>[a-f0-9]{40})$', 'archive'),
)
