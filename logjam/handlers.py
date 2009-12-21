from django.core.handlers import modpython, wsgi, base

class LogJamHandler(base.BaseHandler):
    def handle_uncaught_exception(self, request, resolver, exc_info):
        """
        Sends request to logjam server for recording instead of mailing admins
        
        Be *very* careful when overriding this because the error could be
        caused by anything, so assuming something like the database is always
        available would be an error.
        """
        from django.conf import settings

        if settings.DEBUG_PROPAGATE_EXCEPTIONS:
            raise

        if settings.DEBUG:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)


        from logjam.client import Client, ConnectionError
        try:
            Client().send_exception(request, exc_info)
        except ConnectionError:
            pass
        
        #from django.core.mail import mail_admins
        #subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
        #try:
        #    request_repr = repr(request)
        #except:
        #    request_repr = "Request repr() unavailable"
        #message = "%s\n\n%s" % (self._get_traceback(exc_info), request_repr)
        #mail_admins(subject, message, fail_silently=True)

        # Return an HttpResponse that displays a friendly error message.
        callback, param_dict = resolver.resolve500()
        return callback(request, **param_dict)


class WSGIHandler(LogJamHandler, wsgi.WSGIHandler): pass
class ModPythonHandler(LogJamHandler, modpython.ModPythonHandler): pass
        

