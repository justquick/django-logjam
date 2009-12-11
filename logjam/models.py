from django.db import models

class Exception(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    request = models.TextField()
    traceback = models.TextField()