from django.db import models
import settings


class HttpException(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    exception = models.TextField()
    GET = models.TextField(blank=True)
    POST = models.TextField(blank=True)
    FILES = models.TextField(blank=True)
    COOKIES = models.TextField(blank=True)
    META = models.TextField(blank=True)
    sha = models.CharField(max_length=40, primary_key=settings.UNIQUE)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=6)
    host = models.CharField(max_length=255)
    is_ajax = models.BooleanField(default=False)
    is_secure = models.BooleanField(default=False)
    encoding = models.CharField(max_length=255,default='utf8')

    def last_line(self):
        return filter(None, self.exception.splitlines())[-1]

    def __unicode__(self):
        return u'%s %s - %s' % (self.method, self.exception, self.last_line())